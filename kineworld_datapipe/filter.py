"""Keep clips with enough motion (proxy for physical activity); copy them to a curated dir."""

import shutil
from pathlib import Path

import cv2
from tqdm import tqdm

VIDEO_EXTENSIONS = ("mp4", "mkv", "webm")


def motion_score(path: Path, sample_fps: float = 4.0) -> float:
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    step = max(1, int(fps / sample_fps))
    prev, acc, n = None, 0.0, 0
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % step == 0:
            gray = cv2.cvtColor(cv2.resize(frame, (160, 90)), cv2.COLOR_BGR2GRAY)
            if prev is not None:
                acc += float(cv2.absdiff(gray, prev).mean())
                n += 1
            prev = gray
        idx += 1
    cap.release()
    return acc / n if n else 0.0


def run(in_dir: str, out_dir: str, min_motion: float) -> None:
    src, dst = Path(in_dir), Path(out_dir)
    dst.mkdir(parents=True, exist_ok=True)
    clips = [p for p in src.iterdir() if p.suffix.lstrip(".") in VIDEO_EXTENSIONS]
    kept = 0
    for clip in tqdm(clips, desc="filter"):
        if motion_score(clip) >= min_motion:
            shutil.copy2(clip, dst / clip.name)
            kept += 1
    print(f"[filter] kept {kept}/{len(clips)} clips (min_motion={min_motion})")
