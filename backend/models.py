from enum import Enum

from tortoise import fields
from tortoise.models import Model


class RecipeStatus(str, Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    TRANSCODING = "transcoding"
    ANALYZING = "analyzing"
    EXTRACTING = "extracting"
    COMPLETED = "completed"
    FAILED = "failed"


class Recipe(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=2048)
    title = fields.CharField(max_length=512, null=True)
    status = fields.CharEnumField(RecipeStatus, default=RecipeStatus.PENDING, max_length=32)
    status_text = fields.CharField(max_length=256, default="等待处理...")
    progress = fields.IntField(default=0)
    json_data = fields.JSONField(null=True)
    thumbnail = fields.CharField(max_length=1024, null=True)
    error_message = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "recipes"

    # ── 映射为前端状态 ──

    @property
    def frontend_status(self) -> str:
        mapping = {
            RecipeStatus.PENDING: "processing",
            RecipeStatus.DOWNLOADING: "processing",
            RecipeStatus.TRANSCODING: "processing",
            RecipeStatus.ANALYZING: "generating",
            RecipeStatus.EXTRACTING: "generating",
            RecipeStatus.COMPLETED: "completed",
            RecipeStatus.FAILED: "failed",
        }
        return mapping.get(self.status, "processing")

    @property
    def frontend_status_text(self) -> str:
        mapping = {
            RecipeStatus.PENDING: "排队中...",
            RecipeStatus.DOWNLOADING: "下载视频中...",
            RecipeStatus.TRANSCODING: "转码中...",
            RecipeStatus.ANALYZING: "AI 分析中...",
            RecipeStatus.EXTRACTING: "生成截图中...",
            RecipeStatus.COMPLETED: "已完成",
            RecipeStatus.FAILED: "处理失败",
        }
        return mapping.get(self.status, self.status_text)
