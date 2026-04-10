"""TaskIQ 异步任务 — 视频处理全流程"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

from backend.broker import broker
from backend.config import TORTOISE_ORM, settings
from backend.models import Recipe, RecipeStatus
from backend.utils.dashscope_client import analyze_cooking_video
from backend.utils.video import download_video, extract_frame, transcode_to_720p
from tortoise import Tortoise
from tortoise.exceptions import ConfigurationError

logger = logging.getLogger(__name__)

TAG_COLORS = [
    "bg-secondary-fixed text-on-secondary-fixed",
    "bg-primary-fixed text-on-primary-fixed-variant",
    "bg-tertiary-fixed text-on-tertiary-fixed-variant",
]


async def _update_recipe(recipe_id: int, **kwargs) -> None:
    await Recipe.filter(id=recipe_id).update(**kwargs)


async def _ensure_orm_ready() -> None:
    try:
        _ = Recipe._meta.db
    except ConfigurationError:
        logger.info("Worker ORM 未初始化，正在补做 Tortoise 初始化")
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()


@broker.task
async def process_cooking_video(recipe_id: int, url: str) -> None:
    """
    完整的视频→菜谱异步管线：
    1. yt-dlp 下载
    2. ffmpeg 转码 720p H.264
    3. DashScope 视频推理
    4. ffmpeg 关键帧截图
    5. 资源清理
    """
    await _ensure_orm_ready()

    task_temp_dir = settings.TEMP_DIR / str(recipe_id)
    task_temp_dir.mkdir(parents=True, exist_ok=True)

    raw_path: Path | None = None
    transcoded_path: Path | None = None

    try:
        # ── 阶段 1: 下载 ──
        await _update_recipe(
            recipe_id,
            status=RecipeStatus.DOWNLOADING,
            status_text="正在下载视频...",
            progress=5,
        )
        raw_path = await download_video(url, task_temp_dir)
        await _update_recipe(recipe_id, progress=25)
        logger.info("[%d] 下载完成: %s", recipe_id, raw_path)

        # ── 阶段 2: 转码 ──
        await _update_recipe(
            recipe_id,
            status=RecipeStatus.TRANSCODING,
            status_text="视频转码中 (720p H.264)...",
            progress=30,
        )
        transcoded_path = await transcode_to_720p(raw_path, task_temp_dir)
        await _update_recipe(recipe_id, progress=50)
        logger.info("[%d] 转码完成: %s", recipe_id, transcoded_path)

        # ── 阶段 3: AI 推理 ──
        await _update_recipe(
            recipe_id,
            status=RecipeStatus.ANALYZING,
            status_text="Omni 正在分析转码视频...",
            progress=55,
        )
        recipe_data = await analyze_cooking_video(transcoded_path)
        await _update_recipe(recipe_id, progress=85)
        logger.info("[%d] AI 分析完成, title=%s", recipe_id, recipe_data.get("title"))

        # ── 阶段 4: 截取关键帧 ──
        await _update_recipe(
            recipe_id,
            status=RecipeStatus.EXTRACTING,
            status_text="正在提取关键帧截图...",
            progress=90,
        )

        screenshots_dir = settings.SCREENSHOTS_DIR / str(recipe_id)
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        steps = recipe_data.get("steps", [])
        for step in steps:
            ts = step.get("timestamp")
            if not ts:
                continue
            img_name = f"step_{step['number']}.jpg"
            img_path = screenshots_dir / img_name
            try:
                await extract_frame(transcoded_path, ts, img_path)
                step["image"] = f"/static/screenshots/{recipe_id}/{img_name}"
            except Exception:
                logger.warning("[%d] 截图失败 @%s, 跳过", recipe_id, ts, exc_info=True)
                step["image"] = None

        # 提取缩略图 (视频 1 秒处)
        thumb_path = screenshots_dir / "thumbnail.jpg"
        try:
            await extract_frame(transcoded_path, "00:00:01", thumb_path)
            thumbnail_url = f"/static/screenshots/{recipe_id}/thumbnail.jpg"
        except Exception:
            thumbnail_url = None

        # ── 阶段 5: 持久化结果 ──
        title = recipe_data.get("title", "未命名菜谱")
        category = recipe_data.get("category")
        tag_color = TAG_COLORS[recipe_id % len(TAG_COLORS)]
        recipe_data["tag_color"] = tag_color

        total_words = sum(len(s.get("content", "")) for s in steps)
        total_images = sum(1 for s in steps if s.get("image"))

        await _update_recipe(
            recipe_id,
            status=RecipeStatus.COMPLETED,
            status_text="已完成",
            progress=100,
            title=title,
            thumbnail=thumbnail_url,
            json_data={
                **recipe_data,
                "stats": {"words": total_words, "images": total_images},
            },
        )
        logger.info("[%d] ✓ 任务完成: %s", recipe_id, title)

    except Exception as exc:
        logger.exception("[%d] 任务失败", recipe_id)
        error_message = str(exc)
        if "Omni" in error_message or "DashScope" in error_message:
            error_message = f"Omni 分析失败: {error_message}"
        await _update_recipe(
            recipe_id,
            status=RecipeStatus.FAILED,
            status_text="处理失败",
            error_message=error_message,
        )
    finally:
        # ── 资源清理: 删除 temp 下的原始与中间文件 ──
        if task_temp_dir.exists():
            shutil.rmtree(task_temp_dir, ignore_errors=True)
            logger.info("[%d] 临时文件已清理: %s", recipe_id, task_temp_dir)
