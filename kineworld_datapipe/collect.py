"""Download videos by keyword using yt-dlp."""

import subprocess
from pathlib import Path

VIDEO_EXTENSIONS = ("mp4", "mkv", "webm")


def run(query: str, max_videos: int, out_dir: str) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cmd = [
        "yt-dlp",
        f"ytsearch{max_videos}:{query}",
        "-o", str(out / "%(id)s.%(ext)s"),
        "-f", "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]/best",
        "--merge-output-format", "mp4",
        "--write-info-json",
        "--no-playlist",
    ]
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)
    n = len([p for p in out.iterdir() if p.suffix.lstrip(".") in VIDEO_EXTENSIONS])
    print(f"[collect] {n} videos in {out}")
