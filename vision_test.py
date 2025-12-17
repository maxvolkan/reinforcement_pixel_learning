import mss
import cv2
import numpy as np
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID

windows = CGWindowListCopyWindowInfo(
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID
)

bounds = {}

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

bounds_q = best
print("Using bounds:", bounds_q)

sct = mss.mss()

bounds_mss = {
    "left": int(bounds_q["X"]),
    "top": int(bounds_q["Y"]),
    "width": int(bounds_q["Width"]),
    "height": int(bounds_q["Height"]),
}

while True:
    frame = np.array(sct.grab(bounds_mss))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    cv2.imshow("RotMG View", frame)
    if cv2.waitKey(1) == 27:  # ESC
        break

cv2.destroyAllWindows()
