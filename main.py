# Author: Nazaryan Artem
# Nickname: @slide36

import cv2
import numpy as np
import pyautogui
from os import system as s
from collections import deque
from functions.debug_menu import Debug_menu
from functions.draw_hexagon import draw_hexagon
from functions.detect_fire import detect_fire
from functions.detect_fire_direction import detect_fire_direction

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
DIRECTIONS_QUEUE_MAXLEN = 25
SEGMENT_SIZE = 20
HEXAGON_SIZE = 96

class FireDetection:
    def __init__(self):
        self.dbg = True
        self.show_direction = False
        self.segment_size = SEGMENT_SIZE
        self.hexagon_size = HEXAGON_SIZE
        self.display_mode = 0
        self.prev_center = {}
        self.directions_queue = deque(maxlen=DIRECTIONS_QUEUE_MAXLEN)
        cv2.namedWindow('Fire Detection', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Fire Detection', WINDOW_WIDTH, WINDOW_HEIGHT)

    def run(self):
        while True:
            curr_frame = pyautogui.screenshot()
            curr_frame = np.array(curr_frame)
            curr_frame = curr_frame[:, :, ::-1].copy()

            curr_frame, contours = detect_fire(curr_frame, self.dbg, self.display_mode, self.segment_size)
            if self.show_direction:
                curr_frame = detect_fire_direction(curr_frame, contours, self.prev_center)
            try:
                if self.dbg:
                    self.debug_actions()
            except:
                s('cls')
                print('\n\n\tDebug menu: Off ')

            cv2.imshow('Fire Detection', curr_frame)

            key = cv2.waitKey(1) & 0xFF
            actions = {
                ord('q'): 'exit(0)',
                ord('3'): 'self.show_direction = not self.show_direction',
                ord('9'): 'self.dbg = not self.dbg',
                ord('8'): 'Debug_menu(); print("\tDebug menu: On")'
            }
            
            if key in actions:
                exec(actions[key])

        cv2.destroyAllWindows()

    def debug_actions(self):
        if cv2.getTrackbarPos("RESET", "Trackbars") == 1:
            self.reset_trackbars()
        elif cv2.getTrackbarPos("RESET", "Trackbars") == 1:
            self.config_trackbars()
        elif cv2.getTrackbarPos("PRINT", "Trackbars") == 1:
            self.print_values()
        elif cv2.getTrackbarPos("DMODE", "Trackbars") in [0, 1, 2]:
            self.display_mode = cv2.getTrackbarPos("DMODE", "Trackbars")


    def reset_trackbars(self):
        cv2.setTrackbarPos("LOW_0", "Trackbars", 0)
        cv2.setTrackbarPos("LOW_1", "Trackbars", 100)
        cv2.setTrackbarPos("LOW_2", "Trackbars", 200)
        cv2.setTrackbarPos("HIGH_0", "Trackbars", 15)
        cv2.setTrackbarPos("HIGH_1", "Trackbars", 255)
        cv2.setTrackbarPos("HIGH_2", "Trackbars", 255)
        cv2.setTrackbarPos("RESET", "Trackbars", 0)

    def print_values(self):
        print("Current values:")
        print("LOW:", [cv2.getTrackbarPos(f"LOW_{i}", "Trackbars") for i in range(3)])
        print("HIGH:", [cv2.getTrackbarPos(f"HIGH_{i}", "Trackbars") for i in range(3)])
        cv2.setTrackbarPos("PRINT", "Trackbars", 0)

if __name__ == "__main__":
    fd = FireDetection()
    fd.run()


