"""Video download module - wraps yt-dlp for TikTok."""

import subprocess
import re
from pathlib import Path


def extract_video_id(url: str) -> str | None:
    """Extract TikTok video ID from URL."""
    m = re.search(r'/video/(\d+)', url)
    return m.group(1) if m else None


def download(url: str, out_dir: str | Path, proxy: str | None = None) -> Path | None:
    """Download a TikTok video via yt-dlp.

    Args:
        url: TikTok video URL (tiktok.com/@user/video/xxx)
        out_dir: directory to save the video
        proxy: optional HTTP proxy URL

    Returns:
        Path to downloaded file, or None on failure.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    video_id = extract_video_id(url) or "video"
    template = str(out_dir / f"%(uploader)s_{video_id}.%(ext)s")

    cmd = [
        "yt-dlp",
        "--no-check-certificate",
        "-f", "mp4",
        "-o", template,
        url,
    ]
    if proxy:
        cmd.extend(["--proxy", proxy])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Download failed: {result.stderr[-500:]}")
        return None

    # Find the downloaded file
    files = list(out_dir.glob(f"*_{video_id}.*"))
    return files[0] if files else None
