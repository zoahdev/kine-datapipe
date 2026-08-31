import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kineworld_datapipe.windows import window_for_event, catalog_windows

def test_fits():
    w = window_for_event(40, 100, length=16, margin=1)
    assert w["pre"] == [23, 39]
    assert w["post"] == [41, 57]

def test_too_early():
    assert window_for_event(5, 100, length=16) is None

def test_too_late():
    assert window_for_event(95, 100, length=16) is None

def test_catalog():
    report = {"a.mp4": {"events": [{"frame": 40, "z": 4.2}, {"frame": 3, "z": 5.0}]}}
    rows = catalog_windows(report, {"a.mp4": 100}, length=16)
    assert len(rows) == 1
    assert rows[0]["source"] == "a.mp4"

if __name__ == "__main__":
    test_fits(); test_too_early(); test_too_late(); test_catalog()
    print("PASS test_windows")
