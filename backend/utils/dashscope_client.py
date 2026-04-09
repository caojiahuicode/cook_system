"""DashScope 官方 SDK 集成 — 视频上传与 AI 推理"""

from __future__ import annotations

import asyncio
import json
import logging
import re
from pathlib import Path

import dashscope
from dashscope import MultiModalConversation

from backend.config import settings

logger = logging.getLogger(__name__)

COOKING_ANALYSIS_PROMPT = """\
你是一名专业的美食内容分析 AI。请仔细观看这段烹饪教学视频，提取完整的菜谱信息。

请 **仅** 返回如下严格 JSON（不要添加 ```json 标记或任何多余文字）：
{
  "title": "菜品名称",
  "time": "预计烹饪时长（如：25 分钟）",
  "category": "菜品分类（如：川菜、粤菜、西餐、甜点等）",
  "tags": ["标签1", "标签2"],
  "ingredients": [
    {"name": "食材名称 (含大致用量)", "amount": "精确用量"}
  ],
  "tools": [
    {"name": "厨具名称", "icon": "Material_Symbols_图标名"}
  ],
  "steps": [
    {
      "number": 1,
      "title": "步骤简短标题",
      "content": "详细步骤描述，包含操作方法与注意事项",
      "timestamp": "HH:MM:SS"
    }
  ],
  "tip": "主厨小贴士（综合烹饪要点与窍门）"
}

要求：
1. ingredients 的 name 包含大致用量描述，amount 为精确数值用量
2. tools 的 icon 使用 Google Material Symbols 图标名称（如 skillet, kitchen, oven_gen）
3. steps 的 timestamp 为该步骤在视频中开始出现的准确时间点
4. 步骤描述要详细、专业，包含火候、时间等关键信息
5. 如果无法确定某个字段，请合理推断，不要留空"""


def _build_file_uri(video_path: Path) -> str:
    """构造 DashScope SDK 可接受的本地文件 URI"""
    absolute = video_path.resolve()
    return absolute.as_uri()


def _extract_json(text: str) -> dict:
    """从模型返回文本中提取并校验 JSON"""
    text = text.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence_match:
        text = fence_match.group(1).strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        logger.error("JSON 解析失败，原始文本: %s", text[:500])
        raise ValueError(f"AI 返回的内容不是有效 JSON: {exc}") from exc

    required_keys = {"title", "ingredients", "steps"}
    missing = required_keys - set(data.keys())
    if missing:
        raise ValueError(f"AI 返回 JSON 缺少必要字段: {missing}")

    return data


async def analyze_cooking_video(video_path: Path) -> dict:
    """
    将标准 MP4 上传至 DashScope 临时存储并调用多模态模型分析。

    返回解析后的菜谱 JSON dict。
    """
    dashscope.base_http_api_url = settings.DASHSCOPE_BASE_URL

    file_uri = _build_file_uri(video_path)
    logger.info("DashScope 推理请求 — 模型: %s, 视频: %s", settings.DASHSCOPE_MODEL, file_uri)

    messages = [
        {
            "role": "user",
            "content": [
                {"video": file_uri, "fps": settings.DASHSCOPE_VIDEO_FPS},
                {"text": COOKING_ANALYSIS_PROMPT},
            ],
        }
    ]

    response = await asyncio.to_thread(
        MultiModalConversation.call,
        api_key=settings.DASHSCOPE_API_KEY,
        model=settings.DASHSCOPE_MODEL,
        messages=messages,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"DashScope API 调用失败 (code={response.status_code}): "
            f"{getattr(response, 'message', 'unknown error')}"
        )

    content_list = response.output.choices[0].message.content
    raw_text = ""
    for item in content_list:
        if isinstance(item, dict) and "text" in item:
            raw_text = item["text"]
            break
        elif isinstance(item, str):
            raw_text = item
            break

    if not raw_text:
        raise ValueError("DashScope 返回内容为空")

    logger.info("DashScope 原始响应 (前200字): %s", raw_text[:200])
    return _extract_json(raw_text)
