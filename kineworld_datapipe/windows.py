"""Turn events.json spikes into (pre, post) frame windows.

This is still not a surgical do(); it is the cheapest real-video proxy:
control = the N frames before the spike, intervene = the N frames after.
"""
from __future__ import annotations


def window_for_event(frame: int, total: int, length: int = 16, margin: int = 1):
    """Return (pre_start, pre_end, post_start, post_end) or None if it does not fit."""
    if frame is None:
        return None
    f = int(frame)
    pre_end = f - margin
    pre_start = pre_end - length
    post_start = f + margin
    post_end = post_start + length
    if pre_start < 0 or post_end > total:
        return None
    return {
        "pre": [pre_start, pre_end],
        "post": [post_start, post_end],
        "event_frame": f,
        "length": length,
    }


def catalog_windows(report: dict, totals: dict[str, int], length: int = 16, z_min: float = 3.0):
    rows = []
    n = 0
    for name, entry in sorted(report.items()):
        total = int(totals.get(name, entry.get("frames_sampled", 0)))
        for ev in entry.get("events", []):
            if float(ev.get("z", 0)) < z_min:
                continue
            win = window_for_event(ev.get("frame"), total, length=length)
            if win is None:
                continue
            rows.append({
                "id": f"win-{n:04d}",
                "kind": "motion_spike_window",
                "intervention_id": 2,
                "source": name,
                "z": ev.get("z"),
                **win,
                "note": "pre is control, post is intervene; correlation not causation",
            })
            n += 1
    return rows
