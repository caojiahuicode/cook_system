"""FFmpeg / yt-dlp 视频处理工具函数"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from backend.config import settings

logger = logging.getLogger(__name__)


async def download_video(url: str, output_dir: Path) -> Path:
    """使用 yt-dlp 下载视频，返回下载后的文件路径"""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(output_dir / "%(title).80s.%(ext)s")

    cmd = [
        "yt-dlp",
        "--no-playlist",
        "--no-overwrites",
        "-o", output_template,
        "--print", "after_move:filepath",
        url,
    ]
    logger.info("yt-dlp 开始下载: %s", url)
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(f"yt-dlp 下载失败 (code={proc.returncode}): {stderr.decode(errors='replace')}")

    filepath = stdout.decode(errors="replace").strip().splitlines()[-1]
    logger.info("yt-dlp 下载完成: %s", filepath)
    return Path(filepath)


async def transcode_to_720p(input_path: Path, output_dir: Path) -> Path:
    """
    强制转码为 H.264 720p 30fps MP4
    编码器: libx264 | 分辨率: 1280×720 | 帧率: 30fps
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{input_path.stem}_720p.mp4"

    cmd = [
        settings.FFMPEG_PATH,
        "-i", str(input_path),
        "-c:v", settings.VIDEO_CODEC,
        "-vf", f"scale={settings.VIDEO_WIDTH}:{settings.VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,"
               f"pad={settings.VIDEO_WIDTH}:{settings.VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2",
        "-r", str(settings.VIDEO_FPS),
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        "-y",
        str(output_path),
    ]
    logger.info("ffmpeg 转码开始: %s -> %s", input_path.name, output_path.name)
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg 转码失败 (code={proc.returncode}): {stderr.decode(errors='replace')}")

    logger.info("ffmpeg 转码完成: %s", output_path)
    return output_path


async def extract_frame(video_path: Path, timestamp: str, output_path: Path) -> Path:
    """在指定时间戳截取关键帧图片"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        settings.FFMPEG_PATH,
        "-ss", timestamp,
        "-i", str(video_path),
        "-vframes", "1",
        "-q:v", "2",
        "-y",
        str(output_path),
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg 截图失败 @{timestamp}: {stderr.decode(errors='replace')}")

    logger.info("截图完成: %s @%s", output_path.name, timestamp)
    return output_path


async def get_video_duration(video_path: Path) -> float:
    """获取视频时长 (秒)"""
    cmd = [
        settings.FFMPEG_PATH.replace("ffmpeg", "ffprobe"),
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path),
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    try:
        return float(stdout.decode().strip())
    except ValueError:
        return 0.0
