# Torreta antidrón virtual con objetivos reales

Proyecto final de **Visión por Ordenador I** · 3º Ingeniería Matemática · Universidad Pontificia Comillas ICAI · curso 2026/27.

Una cámara real fija vigila una zona por la que se mueven objetivos físicos (pelotas de colores colgadas como péndulos) que hacen de "drones". El sistema permanece **bloqueado** hasta que el operador muestra a la cámara una secuencia de 4 tarjetas impresas en el orden correcto. Una vez **armado**, detecta y sigue cada objetivo con un filtro de Kalman, y una torreta **virtual** dibujada en pantalla gira, apunta con adelanto y dispara un proyectil virtual cuando prevé un impacto.

Todo es visión por ordenador clásica con Python y OpenCV, sin deep learning y sin hardware adicional.

> **Estado:** primera versión: lectura de la cámara en tiempo real con FPS en pantalla.

## Equipo

| Integrante | Módulo principal |
| --- | --- |
| _Nombre Apellido_ | Calibración y geometría |
| _Nombre Apellido_ | Tarjetas y decodificador |
| _Nombre Apellido_ | Detección y tracking |
| _Nombre Apellido_ | Integración, evaluación y documentación |

Grupo: _A / B_

## Instalación

Requisitos: **Python 3.9** y Git. Las versiones de las librerías son las del entorno de prácticas del curso ([icai-voi/voi-26-27](https://github.com/icai-voi/voi-26-27)); OpenCV 4.8 y NumPy 1.26 no tienen versión para Python 3.13 o superior.

```bash
git clone https://github.com/<usuario>/torreta-antidron.git
cd torreta-antidron

# Windows
py -3.9 -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3.9 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Uso

```bash
python src/main.py            # cámara definida en config/config.yaml
python src/main.py --camera 1 # otra cámara
pytest                        # tests
```

| Tecla | Acción |
| --- | --- |
| `q` / `Esc` | Salir |
| `s` | Guardar el frame actual en `data/snapshots/` |

## Estructura del repositorio

```text
torreta-antidron/
├── src/                # código del sistema
│   ├── main.py         # punto de entrada y bucle en tiempo real
│   ├── camera.py       # captura en un hilo aparte
│   └── fps.py          # FPS y overlay de rendimiento
├── config/config.yaml  # parámetros (cámara, umbrales, código de armado...)
├── calibration/        # imágenes del tablero y resultado calib.yaml
├── tests/              # tests con pytest
├── docs/figures/       # figuras del informe
└── data/               # vídeos y capturas de prueba (no se suben al repo)
```

## Hoja de ruta

- [x] Lectura de la cámara en tiempo real con FPS
- [ ] Calibración offline (K, distorsión, RMS) y corrección de distorsión
- [ ] Detector de tarjetas de armado
- [ ] Decodificador de secuencia (máquina de estados)
- [ ] Detección y tracking multiobjetivo (Kalman + asignación húngara)
- [ ] Control de tiro: torreta virtual, apuntado con adelanto, IFF, radar
- [ ] Evaluación cuantitativa y vídeo demo

## Uso de asistentes de IA

Se ha utilizado Claude (Anthropic) como asistente de diseño y programación. Todo el código ha sido revisado, probado y entendido por el equipo.
