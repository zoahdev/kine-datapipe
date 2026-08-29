"""Download videos by keyword using yt-dlp (YouTube or Bilibili)."""

import http.cookiejar
import subprocess
import urllib.request
from pathlib import Path

VIDEO_EXTENSIONS = ("mp4", "mkv", "webm")
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


def ensure_bili_cookies(cookie_path: Path) -> None:
    """Bilibili's search API rejects cookie-less clients; pick some up from the homepage."""
    if cookie_path.exists() and cookie_path.stat().st_size > 0:
        return
    jar = http.cookiejar.MozillaCookieJar(str(cookie_path))
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = [("User-Agent", USER_AGENT)]
    opener.open("https://www.bilibili.com/", timeout=20)
    jar.save(ignore_discard=True, ignore_expires=True)


def run(query: str, max_videos: int, out_dir: str, source: str = "youtube") -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    if source == "bilibili":
        target = f"bilisearch{max_videos}:{query}"
    else:
        target = f"ytsearch{max_videos}:{query}"
    cmd = [
        "yt-dlp",
        target,
        "-o", str(out / "%(id)s.%(ext)s"),
        "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
        "--merge-output-format", "mp4",
        "--write-info-json",
        "--socket-timeout", "20",
        "--retries", "2",
    ]
    if source == "bilibili":
        cookies = out.parent / "bili-cookies.txt"
        ensure_bili_cookies(cookies)
        cmd += [
            "--cookies", str(cookies),
            "--user-agent", USER_AGENT,
            "--referer", "https://www.bilibili.com",
        ]
    else:
        cmd.append("--no-playlist")
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)
    n = len([p for p in out.iterdir() if p.suffix.lstrip(".") in VIDEO_EXTENSIONS])
    print(f"[collect] {n} videos in {out}")
