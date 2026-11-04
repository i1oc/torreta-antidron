"""Medida de FPS con media móvil exponencial y overlay de rendimiento."""
from __future__ import annotations
import time

import cv2


class FPSCounter:
    """FPS suavizados con una media móvil exponencial (EMA).

    Una EMA evita que el número salte de un frame a otro y es O(1) por frame.
    """

    def __init__(self, alpha: float = 0.1):
        self.alpha = alpha
        self.fps = 0.0
        self._last = None

    def tick(self, now: float | None = None) -> float:
        now = time.perf_counter() if now is None else now
        if self._last is not None:
            dt = now - self._last
            if dt > 0:
                inst = 1.0 / dt
                self.fps = inst if self.fps == 0 else (1 - self.alpha) * self.fps + self.alpha * inst
        self._last = now
        return self.fps


def draw_stats(frame, lines: list[str], origin=(10, 24)) -> None:
    """Dibuja líneas de texto con fondo oscuro para que se lean sobre cualquier imagen."""
    x, y = origin
    for text in lines:
        (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame, (x - 4, y - h - 6), (x + w + 4, y + 6), (0, 0, 0), -1)
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
        y += h + 14
