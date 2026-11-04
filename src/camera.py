"""Captura de vídeo en un hilo aparte.

cap.read() bloquea hasta que llega el siguiente frame. Si se llama en el bucle
principal, el procesado espera a la cámara. Con un hilo dedicado, el bucle
principal siempre recoge el frame más reciente al instante.
"""
from __future__ import annotations

import platform
import threading
import time

import cv2


class ThreadedCamera:
    def __init__(self, index: int = 0, width: int = 640, height: int = 480, fps: int = 30):
        # En Windows, DirectShow abre la cámara más rápido y sin avisos
        backend = cv2.CAP_DSHOW if platform.system() == "Windows" else cv2.CAP_ANY
        self.cap = cv2.VideoCapture(index, backend)
        if not self.cap.isOpened():
            raise RuntimeError(f"No se pudo abrir la cámara {index}. Prueba con otro índice.")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # no acumular frames viejos

        ok, frame = self.cap.read()
        if not ok:
            raise RuntimeError("La cámara se abrió pero no devuelve imágenes.")

        self._frame = frame
        self._frame_id = 0
        self._lock = threading.Lock()
        self._running = True
        self._thread = threading.Thread(target=self._update, daemon=True)
        self._thread.start()

    @property
    def resolution(self) -> tuple[int, int]:
        h, w = self._frame.shape[:2]
        return w, h

    def _update(self) -> None:
        while self._running:
            ok, frame = self.cap.read()
            if not ok:
                time.sleep(0.005)
                continue
            with self._lock:
                self._frame = frame
                self._frame_id += 1

    def read(self):
        """Devuelve (id, frame). El id permite saber si el frame es nuevo."""
        with self._lock:
            return self._frame_id, self._frame

    def release(self) -> None:
        self._running = False
        self._thread.join(timeout=1.0)
        self.cap.release()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.release()
