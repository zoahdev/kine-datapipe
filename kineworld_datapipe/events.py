"""Physical-event mining: detect motion-energy spikes (collision / drop / toppling candidates).

Produces a JSON report so downstream stages (filtering, captioning, benchmark probes)
can focus on physically interesting moments.
"""

import json
from pathlib import Path

import numpy as np

VIDEO_EXTENSIONS = (".mp4", ".mkv", ".webm")


def motion_profile(path, max_frames=300, side=96):
    """Mean absolute frame difference over time, on downscaled grayscale."""
    import cv2

    cap = cv2.VideoCapture(str(path))
    prev, diffs, count = None, [], 0
    while count < max_frames:
        if not cap.grab():
            break
        ok, frame = cap.retrieve()
        if not ok:
            break
        frame = cv2.resize(frame, (side, side))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
        if prev is not None:
            diffs.append(float(np.abs(gray - prev).mean()))
        prev = gray
        count += 1
    cap.release()
    return np.asarray(diffs)


def detect_events(profile, z_thresh=3.0, min_gap=3):
    """Frames whose motion energy exceeds z_thresh standard deviations above the mean."""
    if len(profile) < 8:
        return []
    mu, sd = float(profile.mean()), float(profile.std()) + 1e-9
    z = (profile - mu) / sd
    events, last = [], -10 ** 9
    for i, zi in enumerate(z):
        if zi >= z_thresh and i - last >= min_gap:
            events.append({"frame": int(i + 1), "z": round(float(zi), 2)})
            last = i
    return events


def run(inp, out, z_thresh=3.0):
    inp_dir, out_path = Path(inp), Path(out)
    clips = sorted(
        p for p in inp_dir.iterdir()
        if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS
    )
    if not clips:
        raise FileNotFoundError(f"no video clips found in {inp_dir}")
    report, n_with = {}, 0
    for p in clips:
        profile = motion_profile(p)
        ev = detect_events(profile, z_thresh)
        report[p.name] = {
            "frames_sampled": int(len(profile) + 1),
            "n_events": len(ev),
            "events": ev,
        }
        n_with += bool(ev)
        print(f"{p.name}: {len(ev)} event(s)")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[events] {n_with}/{len(clips)} clips contain motion spikes -> {out_path}")
