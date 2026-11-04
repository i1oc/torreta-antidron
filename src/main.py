"""Punto de entrada del sistema.

Primera versión: lee la cámara en tiempo real y muestra los FPS en cada frame.
Los módulos (calibración, seguridad, tracker, torreta) se irán conectando aquí.

Uso:
    python src/main.py
    python src/main.py --camera 1

Teclas:
    q / ESC  salir
    s        guardar el frame actual en data/snapshots/
"""
import argparse
import time
from pathlib import Path

import cv2
import yaml

from camera import ThreadedCamera
from fps import FPSCounter, draw_stats

ROOT = Path(__file__).resolve().parents[1]


def load_config(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Torreta antidrón virtual")
    p.add_argument("--config", type=Path, default=ROOT / "config" / "config.yaml")
    p.add_argument("--camera", type=int, help="índice de la cámara (sobrescribe la config)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    cfg = load_config(args.config)
    cam_cfg, disp_cfg = cfg["camera"], cfg["display"]
    index = args.camera if args.camera is not None else cam_cfg["index"]

    snapshot_dir = ROOT / disp_cfg["snapshot_dir"]
    window = disp_cfg["window_name"]
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)

    fps = FPSCounter()
    last_id = -1

    with ThreadedCamera(index, cam_cfg["width"], cam_cfg["height"], cam_cfg["fps"]) as cam:
        w, h = cam.resolution
        print(f"Cámara {index} abierta a {w}x{h}. Pulsa 'q' para salir, 's' para capturar.")

        while True:
            frame_id, frame = cam.read()
            if frame_id == last_id:  # aún no hay frame nuevo: no reprocesar el mismo
                if (cv2.waitKey(1) & 0xFF) in (ord("q"), 27):
                    break
                continue
            last_id = frame_id

            t0 = time.perf_counter()
            if cam_cfg.get("mirror", False):
                frame = cv2.flip(frame, 1)
            # --- aquí se conectarán los módulos del sistema ---
            proc_ms = (time.perf_counter() - t0) * 1000

            out = frame.copy()
            draw_stats(out, [f"FPS: {fps.tick():.1f}", f"Proc: {proc_ms:.1f} ms", f"{w}x{h}"])
            cv2.imshow(window, out)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
            if key == ord("s"):
                snapshot_dir.mkdir(parents=True, exist_ok=True)
                name = snapshot_dir / f"snap_{time.strftime('%Y%m%d_%H%M%S')}_{frame_id}.png"
                cv2.imwrite(str(name), frame)  # se guarda sin overlay
                print(f"Guardado {name}")

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
