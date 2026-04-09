"""
API 契约定义 — 接口先行 (Contract First)

所有请求/响应的数据格式在此文件中 100% 定义完毕后，
方可编写任何业务实现代码。
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, HttpUrl


# ────────────────── Request Schemas ──────────────────


class RecipeCreateRequest(BaseModel):
    """提交视频链接，创建转换任务"""
    url: str


# ────────────────── Shared Sub-Schemas ──────────────────


class IngredientSchema(BaseModel):
    name: str
    amount: str


class ToolSchema(BaseModel):
    name: str
    icon: str


class StepSchema(BaseModel):
    number: int
    title: str
    content: str
    image: str | None = None
    timestamp: str | None = None


class TaskStatsSchema(BaseModel):
    words: int
    images: int


# ────────────────── Response Schemas ──────────────────


class RecipeCreateResponse(BaseModel):
    """创建任务后返回"""
    id: int
    status: str


class TaskStatusResponse(BaseModel):
    """Dashboard 任务轮询"""
    id: int
    title: str | None = None
    status: str          # processing | generating | completed | failed
    status_text: str
    progress: int
    time_left: str
    thumbnail: str | None = None
    stats: TaskStatsSchema | None = None
    created_at: datetime


class RecipeDetailResponse(BaseModel):
    """菜谱详情页"""
    id: int
    title: str
    tags: list[str]
    video_link: str
    time: str
    ingredients: list[IngredientSchema]
    tools: list[ToolSchema]
    steps: list[StepSchema]
    tip: str
    category: str | None = None
    created_at: datetime


class RecipeListItem(BaseModel):
    """做饭库列表项"""
    id: int
    title: str
    category: str | None = None
    date: str
    time: str
    image: str | None = None
    tag_color: str


class RecipeListResponse(BaseModel):
    recipes: list[RecipeListItem]
    total: int


class ErrorResponse(BaseModel):
    detail: str
