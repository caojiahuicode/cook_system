"""FastAPI 入口 — 厨神笔记后端"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from backend.broker import broker
from backend.config import TORTOISE_ORM, settings
from backend.models import Recipe, RecipeStatus
from backend.schemas import (
    RecipeCreateRequest,
    RecipeCreateResponse,
    RecipeDetailResponse,
    RecipeListItem,
    RecipeListResponse,
    TaskStatusResponse,
)
from backend.tasks import process_cooking_video

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ────────────────── App Lifespan ──────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.STATIC_DIR.mkdir(parents=True, exist_ok=True)
    settings.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    settings.TEMP_DIR.mkdir(parents=True, exist_ok=True)

    if not broker.is_worker_process:
        await broker.startup()
    yield
    if not broker.is_worker_process:
        await broker.shutdown()


app = FastAPI(title="厨神笔记 API", version="1.0.0", lifespan=lifespan)

# ── CORS (开发阶段允许前端 dev server) ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 静态文件 ──
settings.STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

# ── Tortoise ORM ──
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)


# ────────────────── API Routes ──────────────────


@app.post("/api/recipes", response_model=RecipeCreateResponse, status_code=201)
async def create_recipe(req: RecipeCreateRequest):
    """提交视频链接，创建异步转换任务"""
    recipe = await Recipe.create(url=req.url)
    await process_cooking_video.kiq(recipe.id, req.url)
    logger.info("新任务已入队: id=%d url=%s", recipe.id, req.url)
    return RecipeCreateResponse(id=recipe.id, status=recipe.frontend_status)


@app.get("/api/tasks", response_model=list[TaskStatusResponse])
async def list_tasks():
    """获取所有任务状态 (Dashboard 轮询)"""
    recipes = await Recipe.all().order_by("-created_at").limit(50)
    return [_build_task_status(r) for r in recipes]


@app.get("/api/recipes", response_model=RecipeListResponse)
async def list_recipes(category: str | None = None):
    """获取已完成的菜谱列表 (做饭库)"""
    qs = Recipe.filter(status=RecipeStatus.COMPLETED)
    if category and category != "全部":
        qs = qs.filter(json_data__contains={"category": category})
    recipes = await qs.order_by("-created_at").all()
    items = [_build_list_item(r) for r in recipes]
    return RecipeListResponse(recipes=items, total=len(items))


@app.get("/api/recipes/{recipe_id}", response_model=RecipeDetailResponse)
async def get_recipe(recipe_id: int):
    """获取菜谱详情"""
    recipe = await Recipe.get_or_none(id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="菜谱不存在")
    if recipe.status != RecipeStatus.COMPLETED or not recipe.json_data:
        raise HTTPException(status_code=404, detail="菜谱尚未完成处理")
    return _build_detail(recipe)


@app.get("/api/recipes/{recipe_id}/status", response_model=TaskStatusResponse)
async def get_recipe_status(recipe_id: int):
    """轮询单个任务状态"""
    recipe = await Recipe.get_or_none(id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="任务不存在")
    return _build_task_status(recipe)


@app.delete("/api/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int):
    """删除菜谱"""
    deleted = await Recipe.filter(id=recipe_id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="菜谱不存在")
    return {"ok": True}


# ────────────────── Helper Builders ──────────────────


def _build_task_status(recipe: Recipe) -> TaskStatusResponse:
    data = recipe.json_data or {}
    stats = data.get("stats")
    time_left_map = {
        RecipeStatus.PENDING: "排队等待中",
        RecipeStatus.DOWNLOADING: "预计剩余 3 分钟",
        RecipeStatus.TRANSCODING: "预计剩余 2 分钟",
        RecipeStatus.ANALYZING: "正在生成图文食谱",
        RecipeStatus.EXTRACTING: "即将完成",
        RecipeStatus.COMPLETED: "已保存至做饭库",
        RecipeStatus.FAILED: "处理失败",
    }
    return TaskStatusResponse(
        id=recipe.id,
        title=recipe.title,
        status=recipe.frontend_status,
        status_text=recipe.frontend_status_text,
        progress=recipe.progress,
        time_left=time_left_map.get(recipe.status, "处理中..."),
        thumbnail=recipe.thumbnail,
        stats=stats if stats else None,
        created_at=recipe.created_at,
    )


def _build_list_item(recipe: Recipe) -> RecipeListItem:
    data = recipe.json_data or {}
    return RecipeListItem(
        id=recipe.id,
        title=recipe.title or "未命名菜谱",
        category=data.get("category"),
        date=recipe.created_at.strftime("%Y年%m月%d日"),
        time=data.get("time", "未知"),
        image=recipe.thumbnail,
        tag_color=data.get("tag_color", "bg-primary-fixed text-on-primary-fixed-variant"),
    )


def _build_detail(recipe: Recipe) -> RecipeDetailResponse:
    data = recipe.json_data or {}
    return RecipeDetailResponse(
        id=recipe.id,
        title=data.get("title", recipe.title or "未命名菜谱"),
        tags=data.get("tags", []),
        video_link=recipe.url,
        time=data.get("time", "未知"),
        ingredients=data.get("ingredients", []),
        tools=data.get("tools", []),
        steps=data.get("steps", []),
        tip=data.get("tip", ""),
        category=data.get("category"),
        created_at=recipe.created_at,
    )
