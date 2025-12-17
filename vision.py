# vision.py
import mss
import cv2
import numpy as np
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID,
)

class Vision:
    def __init__(self):
        windows = CGWindowListCopyWindowInfo(
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID
        )

        best = None
        best_area = 0

        for w in windows:
            name = w.get("kCGWindowName", "")
            owner = w.get("kCGWindowOwnerName", "")

            if "RotMG" in owner or "RotMG" in name:
                b = w["kCGWindowBounds"]
                area = b["Width"] * b["Height"]

                if area > best_area:
                    best_area = area
                    best = b

        if best is None:
            raise RuntimeError("RotMG window not found")

        self.bounds_q = best
        print("Using bounds:", self.bounds_q)

        self.sct = mss.mss()
        self.bounds_mss = {
            "left": int(self.bounds_q["X"]),
            "top": int(self.bounds_q["Y"]),
            "width": int(self.bounds_q["Width"]),
            "height": int(self.bounds_q["Height"]),
        }

    def get_frame(self):
        frame = np.array(self.sct.grab(self.bounds_mss))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        return frame

    @property
    def width(self):
        return self.bounds_mss["width"]

    @property
    def height(self):
        return self.bounds_mss["height"]
