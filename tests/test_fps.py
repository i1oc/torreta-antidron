import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fps import FPSCounter  # noqa: E402


def test_fps_converges_to_constant_rate():
    counter = FPSCounter(alpha=0.2)
    t = 0.0
    for _ in range(100):
        counter.tick(t)
        t += 1 / 30
    assert abs(counter.fps - 30) < 0.1


def test_first_tick_returns_zero():
    assert FPSCounter().tick(0.0) == 0.0
