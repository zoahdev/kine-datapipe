"""Emit a catalog of control/intervene clip pairs for KINE-EXP-002."""
from __future__ import annotations
import json
from pathlib import Path

from .windows import catalog_windows


def synthetic_catalog(n: int = 200) -> list[dict]:
    return [{
        "id": f"syn-{i:04d}",
        "kind": "remove_support",
        "intervention_id": 1,
        "source": "synthetic",
        "control": {"seed": i, "falling": False},
        "intervene": {"seed": i, "falling": True},
    } for i in range(n)]


def from_events(events_path: Path, z_min: float = 3.0, length: int = 16) -> list[dict]:
    if not events_path.is_file():
        return []
    report = json.loads(events_path.read_text(encoding="utf-8"))
    totals = {name: int(entry.get("frames_sampled", 0)) for name, entry in report.items()}
    return catalog_windows(report, totals, length=length, z_min=z_min)


def run(out: str, n_synthetic: int = 200, events: str | None = None, length: int = 16) -> None:
    outp = Path(out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    rows = synthetic_catalog(n_synthetic)
    n_evt = 0
    if events:
        extra = from_events(Path(events), length=length)
        n_evt = len(extra)
        rows.extend(extra)
    payload = {"version": "0.2", "n": len(rows), "n_synthetic": n_synthetic, "n_event_windows": n_evt, "pairs": rows}
    outp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[pairs] wrote {len(rows)} rows (synthetic={n_synthetic} windows={n_evt}) -> {outp}")
