# Air Mouse

Control your computer pointer **hands-free** using just your webcam and intuitive hand gestures.

---

## Features
* **Cursor control** – Join your index and middle finger and then move them to move the mouse pointer in real-time.
* **Left click** – Touch your **index finger** and **thumb** tips together.
* **Right click** – Touch your **middle finger** and **thumb** tips together.
* **Gesture based activation** – Mouse actions trigger only when your palm faces the camera to avoid accidental clicks.
* **Smooth motion** – A custom moving-average smoother eliminates jitter for a natural feel.
* **Cross-platform Python** – Core CV logic uses [MediaPipe Hands](https://developers.google.com/mediapipe) and OpenCV, tested on Windows.

## Demo

You can see the demo here:
https://github.com/user-attachments/assets/5bc6141f-73c1-4a0b-863e-2a818e9acc57

## Installation
> Tested with **Python 3.10+** on Windows 10/11.

```bash
# 1. Clone the repository
$ git clone https://github.com/<your-username>/air-mouse.git
$ cd air-mouse

# 2. (Recommended) Create a virtual environment
$ python -m venv .venv
$ .venv\Scripts\activate          # PowerShell (Windows)

# 3. Install dependencies
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

### Extra requirements
* A working **webcam**.
* Administrative privileges may be required the first time the script accesses low-level mouse APIs.

## Usage
```bash
# From the project root
$ python main.py
```

The webcam feed will open.  Keep your hand ~40-70 cm away from the camera.

* Press **q** to quit.

## Configuration
Runtime settings live in [`config.py`](./config.py):

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_NUM_HANDS` | 2 | Detect up to N hands. |
| `MIN_DETECTION_CONFIDENCE` | 0.5 | Confidence threshold for detection step. |
| `MIN_TRACKING_CONFIDENCE` | 0.5 | Confidence threshold for landmark tracking. |
| `SHOW_IMAGE` | `True` | Show annotated webcam window. |

You can also tweak mouse sensitivity in `mouse_handler/mouse_handler.py` (`mouse_sensi` argument).

## Project Structure
```
Air_Mouse/
├─ camera_handler/          # Webcam capture & preprocessing
│  └─ camera.py
├─ detector/                # MediaPipe hand-tracking wrapper
│  ├─ detector.py
│  └─ models.py
├─ mouse_handler/           # OS-level mouse utilities & gesture logic
│  ├─ mouse_handler.py
│  └─ helper.py
├─ config.py                # Global configuration flags
├─ main.py                  # Application entry-point
├─ requirements.txt         # Python dependencies
└─ README.md                # ← you are here
```

## License
This project is released under the MIT License.
