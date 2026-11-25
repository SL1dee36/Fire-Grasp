# Author: Nazaryan Artem
# Nickname: @slide36

from collections import deque
import cv2

from functions.debug_menu import Debug_menu
from functions.detect_fire import (
    DILATE_ITERATIONS,
    ERODE_ITERATIONS,
    KERNEL_SIZE,
    OUTLINE_INDEX_MAP,
    detect_fire,
)
from functions.detect_fire_direction import detect_fire_direction
from functions.utils import capture_screen, load_fire_bounds

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
DIRECTIONS_QUEUE_MAXLEN = 25
SEGMENT_SIZE = 20
HEXAGON_SIZE = 96
OUTLINE_TYPE = "SURFACE AREA"  # SURFACE AREA, RECTANGLE, HEXAGON


class FireDetection:
    def __init__(self):
        self.dbg = False
        self.show_direction = False
        self.segment_size = SEGMENT_SIZE
        self.hexagon_size = HEXAGON_SIZE
        self.outline_type = OUTLINE_TYPE
        self.kernel_size = KERNEL_SIZE
        self.dilate_iterations = DILATE_ITERATIONS
        self.erode_iterations = ERODE_ITERATIONS
        self.prev_center = {}
        self.directions_queue = deque(maxlen=DIRECTIONS_QUEUE_MAXLEN)

        lower, upper = load_fire_bounds()
        self.l_h, self.l_s, self.l_v = lower
        self.h_h, self.h_s, self.h_v = upper

        cv2.namedWindow("Fire Detection", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Fire Detection", WINDOW_WIDTH, WINDOW_HEIGHT)

    def _toggle_direction(self):
        self.show_direction = not self.show_direction

    def _toggle_debug(self):
        self.dbg = not self.dbg
        print(f"\tDebug menu: {'On' if self.dbg else 'Off'}")

    def _open_debug_menu(self):
        outline_idx = next(
            (k for k, v in OUTLINE_INDEX_MAP.items() if v == str(self.outline_type).upper()),
            0,
        )
        Debug_menu(
            lower=(self.l_h, self.l_s, self.l_v),
            upper=(self.h_h, self.h_s, self.h_v),
            outline_idx=outline_idx,
        )
        self.dbg = True
        print("\tDebug menu: On")

    def run(self):
        actions = {
            ord("3"): self._toggle_direction,
            ord("9"): self._toggle_debug,
            ord("8"): self._open_debug_menu,
        }

        try:
            while True:
                curr_frame = capture_screen()
                curr_frame, contours = detect_fire(
                    curr_frame,
                    self.dbg,
                    self.outline_type,
                    self.hexagon_size,
                    (self.l_h, self.l_s, self.l_v),
                    (self.h_h, self.h_s, self.h_v),
                    self.dilate_iterations,
                    self.erode_iterations,
                    kernel_size=self.kernel_size,
                )
                if self.show_direction:
                    curr_frame = detect_fire_direction(curr_frame, contours, self.prev_center)

                if self.dbg:
                    self.debug_actions()

                cv2.imshow("Fire Detection", curr_frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                if key in actions:
                    actions[key]()

                if cv2.getWindowProperty("Fire Detection", cv2.WND_PROP_VISIBLE) < 1:
                    break
        finally:
            cv2.destroyAllWindows()

    def debug_actions(self):
        try:
            if cv2.getWindowProperty("Trackbars", cv2.WND_PROP_VISIBLE) < 1:
                return
            if cv2.getTrackbarPos("RESET", "Trackbars") == 1:
                self.reset_trackbars()
            elif cv2.getTrackbarPos("PRINT", "Trackbars") == 1:
                self.print_values()

            outline_idx = cv2.getTrackbarPos("OUTLINE", "Trackbars")
            if outline_idx in OUTLINE_INDEX_MAP:
                self.outline_type = OUTLINE_INDEX_MAP[outline_idx]
        except cv2.error:
            pass

    def reset_trackbars(self):
        defaults_low = (0, 100, 200)
        defaults_high = (15, 255, 255)
        self.l_h, self.l_s, self.l_v = defaults_low
        self.h_h, self.h_s, self.h_v = defaults_high

        for i, val in enumerate(defaults_low):
            cv2.setTrackbarPos(f"LOW_{i}", "Trackbars", val)
        for i, val in enumerate(defaults_high):
            cv2.setTrackbarPos(f"HIGH_{i}", "Trackbars", val)
        cv2.setTrackbarPos("RESET", "Trackbars", 0)

    def print_values(self):
        print("Current values:")
        print("LOW:", [cv2.getTrackbarPos(f"LOW_{i}", "Trackbars") for i in range(3)])
        print("HIGH:", [cv2.getTrackbarPos(f"HIGH_{i}", "Trackbars") for i in range(3)])
        cv2.setTrackbarPos("PRINT", "Trackbars", 0)


if __name__ == "__main__":
    fd = FireDetection()
    fd.run()
