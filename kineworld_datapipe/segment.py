"""Split videos into clips at scene cuts using OpenCV frame differencing."""

from pathlib import Path

import cv2
from tqdm import tqdm

VIDEO_EXTENSIONS = ("mp4", "mkv", "webm")


def scene_boundaries(path: Path, threshold: float = 30.0, sample_fps: float = 4.0):
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    step = max(1, int(fps / sample_fps))
    prev = None
    boundaries = [0.0]
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % step == 0:
            gray = cv2.cvtColor(cv2.resize(frame, (160, 90)), cv2.COLOR_BGR2GRAY)
            if prev is not None:
                diff = float(cv2.absdiff(gray, prev).mean())
                if diff > threshold:
                    boundaries.append(idx / fps)
            prev = gray
        idx += 1
    cap.release()
    boundaries.append(idx / fps)
    return boundaries


def run(in_dir: str, out_dir: str, min_len: float, max_len: float) -> None:
    src, dst = Path(in_dir), Path(out_dir)
    dst.mkdir(parents=True, exist_ok=True)
    videos = [p for p in src.iterdir() if p.suffix.lstrip(".") in VIDEO_EXTENSIONS]
    for video in tqdm(videos, desc="segment"):
        bounds = scene_boundaries(video)
        start = 0.0
        clip_idx = 0
        for end in bounds[1:]:
            if end - start >= max_len:
                _cut(video, dst, clip_idx, start, start + max_len)
                clip_idx += 1
                start += max_len
            elif end - start >= min_len:
                _cut(video, dst, clip_idx, start, end)
                clip_idx += 1
                start = end
    print(f"[segment] clips written to {dst}")


def _cut(video: Path, dst: Path, idx: int, start: float, end: float) -> None:
    import subprocess

    out = dst / f"{video.stem}_c{idx:04d}.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-ss", f"{start:.2f}", "-to", f"{end:.2f}", "-i", str(video),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
            "-c:a", "aac", str(out),
        ],
        check=True,
    )
