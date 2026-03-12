from __future__ import annotations

import re
import time
from pathlib import Path

from picarx import Picarx


TXT_FILE = Path("/home/charles/ai-pet/stt/whisper.cpp/samples/test16k.wav.txt")
POLL_SECONDS = 1.0
FORWARD_SECONDS = 1.2
FORWARD_SPEED = 35
BACKWARD_SECONDS = 1.0
BACKWARD_SPEED = 30
LEFT_FORWARD_SECONDS = 0.9
LEFT_STEER_ANGLE = -30
RIGHT_FORWARD_SECONDS = 0.9
RIGHT_STEER_ANGLE = 30
CAM_UP_ANGLE = 90


def move_forward_briefly(px: Picarx, speed: int, seconds: float) -> None:
    """Move forward for a short duration, then stop."""
    try:
        px.forward(speed)
        time.sleep(seconds)
    finally:
        px.stop()


def move_backward_briefly(px: Picarx, speed: int, seconds: float) -> None:
	"""Move backward for a short duration, then stop."""
	try:
		px.backward(speed)
		time.sleep(seconds)
	finally:
		px.stop()


def move_forward_left_briefly(px: Picarx, speed: int, seconds: float, angle: int) -> None:
	"""Steer left while moving forward, then stop and center steering."""
	try:
		px.set_dir_servo_angle(angle)
		px.forward(speed)
		time.sleep(seconds)
	finally:
		px.stop()
		px.set_dir_servo_angle(0)


def move_forward_right_briefly(px: Picarx, speed: int, seconds: float, angle: int) -> None:
	"""Steer right while moving forward, then stop and center steering."""
	try:
		px.set_dir_servo_angle(angle)
		px.forward(speed)
		time.sleep(seconds)
	finally:
		px.stop()
		px.set_dir_servo_angle(0)


def move_camera_upper(px: Picarx, angle: int) -> None:
    """Move camera upward; use tilt if available, fallback to pan."""
    try:
        px.set_cam_tilt_angle(angle)
    except Exception:
        px.set_cam_pan_angle(angle)


def clear_text_file(path: Path) -> None:
    path.write_text("", encoding="utf-8")


def has_forward_command(text: str) -> bool:
    return re.search(r"\b(front|go go|move|come)\b", text.lower()) is not None


def has_backward_command(text: str) -> bool:
	return re.search(r"\b(back|away)\b", text.lower()) is not None


def has_left_command(text: str) -> bool:
	return re.search(r"\bleft\b", text.lower()) is not None


def has_right_command(text: str) -> bool:
	return re.search(r"\bright\b", text.lower()) is not None


def main() -> None:
	px = Picarx()
	print(f"Listening to {TXT_FILE} every {POLL_SECONDS:.0f}s (Ctrl+C to stop)")

	while True:
		try:
			if TXT_FILE.exists():
				text = TXT_FILE.read_text(encoding="utf-8").strip()
				if text and has_left_command(text):
					print(f"Command detected: {text!r} -> forward + left")
					move_camera_upper(px, CAM_UP_ANGLE)
					move_forward_left_briefly(
						px, FORWARD_SPEED, LEFT_FORWARD_SECONDS, LEFT_STEER_ANGLE
					)
					clear_text_file(TXT_FILE)
					print("Left move complete. Cleared command file.")
				elif text and has_right_command(text):
					print(f"Command detected: {text!r} -> forward + right")
					move_camera_upper(px, CAM_UP_ANGLE)
					move_forward_right_briefly(
						px, FORWARD_SPEED, RIGHT_FORWARD_SECONDS, RIGHT_STEER_ANGLE
					)
					clear_text_file(TXT_FILE)
					print("Right move complete. Cleared command file.")
				elif text and has_forward_command(text):
					print(f"Command detected: {text!r} -> moving forward")
					move_camera_upper(px, CAM_UP_ANGLE)
					move_forward_briefly(px, FORWARD_SPEED, FORWARD_SECONDS)
					clear_text_file(TXT_FILE)
					print("Move complete. Cleared command file.")
				elif text and has_backward_command(text):
					print(f"Command detected: {text!r} -> moving backward")
					move_backward_briefly(px, BACKWARD_SPEED, BACKWARD_SECONDS)
					clear_text_file(TXT_FILE)
					print("Reverse complete. Cleared command file.")
			time.sleep(POLL_SECONDS)
		except KeyboardInterrupt:
			print("Stopped by user")
			px.stop()
			break
		except Exception as exc:
			# Keep loop alive on transient file/hardware errors.
			print(f"Loop error: {exc}")
			time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
