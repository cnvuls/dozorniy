import base64
import os
import platform
import subprocess
from typing import Optional, Tuple

import cv2
import mss
import numpy as np


def get_primary_wayland_display() -> Optional[str]:
    try:
        proc = subprocess.run(["wlr-randr"], capture_output=True, text=True, check=True)
        for line in proc.stdout.splitlines():
            if line and not line.startswith(" "):
                return line.split()[0]
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return None


def capture_screen(target_size: Optional[Tuple[int, int]] = None) -> np.ndarray:
    system = platform.system().lower()

    if system == "windows":
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            raw_bgra = np.array(sct_img)

            bgr_frame = cv2.cvtColor(raw_bgra, cv2.COLOR_BGRA2BGR)
            if bgr_frame is None:
                raise RuntimeError("OpenCV cvtColor вернул None на Windows")

            if target_size is None:
                return bgr_frame

            resized_frame = cv2.resize(
                bgr_frame, target_size, interpolation=cv2.INTER_AREA
            )
            if resized_frame is None:
                raise RuntimeError("OpenCV resize вернул None на Windows")

            return resized_frame

    elif system == "linux":
        is_wayland = os.environ.get("XDG_SESSION_TYPE") == "wayland"

        if is_wayland:
            display_name = get_primary_wayland_display()
            cmd = (
                ["grim", "-o", display_name, "-t", "ppm", "-"]
                if display_name
                else ["grim", "-t", "ppm", "-"]
            )

            try:
                proc = subprocess.run(cmd, capture_output=True, check=True)
            except Exception as e:
                raise RuntimeError(f"Grim capture failed: {e}")

            nparr = np.frombuffer(proc.stdout, np.uint8)

            decoded = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if decoded is None:
                raise ValueError("Не удалось декодировать кадр от grim")

            if not display_name:
                h, w = decoded.shape[:2]
                if w > h * 2.5:
                    decoded = decoded[:, : w // 2]

            if target_size is None:
                return decoded

            resized_frame = cv2.resize(
                decoded, target_size, interpolation=cv2.INTER_AREA
            )
            if resized_frame is None:
                raise RuntimeError("OpenCV resize вернул None на Wayland")

            return resized_frame

        with mss.mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            raw_bgra = np.array(sct_img)

            bgr_frame = cv2.cvtColor(raw_bgra, cv2.COLOR_BGRA2BGR)
            if bgr_frame is None:
                raise RuntimeError("OpenCV cvtColor вернул None на X11")

            if target_size is None:
                return bgr_frame

            resized_frame = cv2.resize(
                bgr_frame, target_size, interpolation=cv2.INTER_AREA
            )
            if resized_frame is None:
                raise RuntimeError("OpenCV resize вернул None на X11")

            return resized_frame

    else:
        raise OSError(f"ОС {system} не поддерживается")


def to_base64(frame: np.ndarray, quality: int = 80) -> str:
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    success, buffer = cv2.imencode(".jpg", frame, encode_param)

    if not success:
        raise ValueError("Ошибка кодирования JPEG")

    return base64.b64encode(buffer).decode("utf-8")
