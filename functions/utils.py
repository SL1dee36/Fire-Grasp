import ast
import threading
from pathlib import Path

import cv2
import numpy as np

try:
    import mss
except ImportError:
    mss = None

import pyautogui

ROOT_DIR = Path(__file__).resolve().parent.parent
FIRE_DATA_PATH = ROOT_DIR / "tools" / "FireDatas.txt"

DEFAULT_LOWER_HSV = (5, 65, 145)
DEFAULT_UPPER_HSV = (30, 255, 255)

_thread_local = threading.local()


def capture_screen():
    """Capture the primary screen and return a BGR numpy array."""
    if mss is not None:
        try:
            sct = getattr(_thread_local, "sct", None)
            if sct is None:
                sct = mss.mss()
                _thread_local.sct = sct
            monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
            raw = np.asarray(sct.grab(monitor))
            return cv2.cvtColor(raw, cv2.COLOR_BGRA2BGR)
        except Exception:
            _thread_local.sct = None

    screenshot = pyautogui.screenshot()
    frame = np.asarray(screenshot)
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)


def _parse_hsv_tuple(line):
    values = ast.literal_eval(line.strip())
    if not isinstance(values, (list, tuple)) or len(values) != 3:
        raise ValueError("Expected 3 HSV components")
    parsed = tuple(int(v) for v in values)
    if any(v < 0 or v > 255 for v in parsed):
        raise ValueError("HSV components must be in range 0..255")
    return parsed


def load_fire_bounds(path=FIRE_DATA_PATH):
    """Load (lower, upper) HSV tuples from FireDatas.txt, or return defaults."""
    file_path = Path(path)
    if not file_path.is_file():
        return DEFAULT_LOWER_HSV, DEFAULT_UPPER_HSV
    try:
        lines = [line.strip() for line in file_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(lines) < 2:
            return DEFAULT_LOWER_HSV, DEFAULT_UPPER_HSV
        return _parse_hsv_tuple(lines[0]), _parse_hsv_tuple(lines[1])
    except Exception:
        return DEFAULT_LOWER_HSV, DEFAULT_UPPER_HSV


def save_fire_bounds(lower, upper, path=FIRE_DATA_PATH):
    """Persist (lower, upper) HSV bounds to FireDatas.txt."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    lower_list = [int(v) for v in lower]
    upper_list = [int(v) for v in upper]
    file_path.write_text(f"{lower_list}\n{upper_list}\n", encoding="utf-8")
