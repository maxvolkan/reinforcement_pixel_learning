import time
import cv2
import numpy as np
from pynput.keyboard import Controller
from vision import Vision

kbd = Controller()
vision = Vision()

WIDTH = vision.width
HEIGHT = vision.height
SCREEN_CENTER = (WIDTH // 2, HEIGHT // 2)

def compute_motion(prev_frame, curr_frame):
    g1 = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(g1, g2)
    motion = diff.mean()

    return motion > 2.0, motion


def frame_energy(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray.std()


def press_keys(keys, duration=0.05):
    for k in keys:
        kbd.press(k)
    time.sleep(duration)
    for k in keys:
        kbd.release(k)

# main loop for code
prev_frame = None
t0 = time.time()
step = 0

while True:
    frame = vision.get_frame()
    now = time.time()

    moving = False
    motion_amount = 0.0

    if prev_frame is not None:
        moving, motion_amount = compute_motion(prev_frame, frame)

    energy = frame_energy(frame)

    # log output, WE SHOULD USE THIS FOR TRAINING
    print({
        "step": step,
        "time": round(now - t0, 3),
        "moving": moving,
        "motion": round(motion_amount, 2),
        "frame_energy": round(energy, 2),
    })

    # chagne to random mvmt later
    if step % 30 == 0:
        press_keys(['w'], 0.05)

    cv2.putText(
        frame,
        f"moving={moving} motion={motion_amount:.2f}",
        (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        1,
    )

    cv2.imshow("RotMG Bot View", frame)
    if cv2.waitKey(1) == 27:  # ESC
        break

    prev_frame = frame.copy()
    step += 1

cv2.destroyAllWindows()
