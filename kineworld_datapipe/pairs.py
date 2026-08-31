"""Emit a catalog of control/intervene clip pairs for KINE-EXP-002.

This does not invent labels from raw internet video. It writes a JSON
catalog that downstream loaders can fill from:
  1) synthetic falling-block pairs (always available)
  2) later: events.json windows around drop/collision spikes
"""
from __future__ import annotations
import json
from pathlib import Path


def synthetic_catalog(n: int = 200) -> list[dict]:
    rows = []
    for i in range(n):
        rows.append({
            "id": f"syn-{i:04d}",
            "kind": "remove_support",
            "intervention_id": 1,
            "source": "synthetic",
            "control": {"seed": i, "falling": False},
            "intervene": {"seed": i, "falling": True},
        })
    return rows


def from_events(events_path: Path, z_min: float = 3.0) -> list[dict]:
    if not events_path.is_file():
        return []
    report = json.loads(events_path.read_text(encoding="utf-8"))
    rows = []
    n = 0
    for name, entry in sorted(report.items()):
        for ev in entry.get("events", []):
            if float(ev.get("z", 0)) < z_min:
                continue
            rows.append({
                "id": f"evt-{n:04d}",
                "kind": ev.get("type", "motion_spike"),
                "intervention_id": 2,
                "source": name,
                "frame": ev.get("frame"),
                "note": "pre-window is control, post-window is intervene; not yet a true do() pair",
            })
            n += 1
    return rows


def run(out: str, n_synthetic: int = 200, events: str | None = None) -> None:
    outp = Path(out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    rows = synthetic_catalog(n_synthetic)
    if events:
        rows.extend(from_events(Path(events)))
    payload = {"version": "0.1", "n": len(rows), "pairs": rows}
    outp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[pairs] wrote {len(rows)} rows -> {outp}")
