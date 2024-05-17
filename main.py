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

dbg = True
show_direction = False

# размер сегмента
segment_size = 2

# Размер гексагона
hexagon_size = 296

# режим отображения (0 - контур, 1 - квадраты, 2 - гексагоны)
display_mode = 0

# Измените prev_center на словарь, чтобы отслеживать движение каждого контура
prev_center = {}

# Инициализация очереди для хранения последних N направлений движения
directions_queue = deque(maxlen=25)

# создание окна для отображения результатов
cv2.namedWindow('Fire Detection', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Fire Detection', 1280, 720)

#Debug_menu()

# бесконечный цикл для обнаружения огня в реальном времени
while True:
    curr_frame = pyautogui.screenshot()
    curr_frame = np.array(curr_frame)
    curr_frame = curr_frame[:, :, ::-1].copy()

    curr_frame, contours = detect_fire(curr_frame, dbg, display_mode, segment_size)
    if show_direction:
        curr_frame = detect_fire_direction(curr_frame, contours, prev_center)
    try:
        if dbg == True:
            if cv2.getTrackbarPos("RESET", "Trackbars") == 1:
                cv2.setTrackbarPos("LOW_0", "Trackbars", 0)
                cv2.setTrackbarPos("LOW_1", "Trackbars", 100)
                cv2.setTrackbarPos("LOW_2", "Trackbars", 200)
                cv2.setTrackbarPos("HIGH_0", "Trackbars", 15)
                cv2.setTrackbarPos("HIGH_1", "Trackbars", 255)
                cv2.setTrackbarPos("HIGH_2", "Trackbars", 255)
                cv2.setTrackbarPos("RESET", "Trackbars", 0)

            elif cv2.getTrackbarPos("PRINT", "Trackbars") == 1:
                print("Current values:")
                print("LOW:", [cv2.getTrackbarPos(f"LOW_{i}", "Trackbars") for i in range(3)])
                print("HIGH:", [cv2.getTrackbarPos(f"HIGH_{i}", "Trackbars") for i in range(3)])
                cv2.setTrackbarPos("PRINT", "Trackbars", 0)

            elif cv2.getTrackbarPos("DMODE", "Trackbars") == 0:
                display_mode = 0
            elif cv2.getTrackbarPos("DMODE", "Trackbars") == 1:
                display_mode = 1
            elif cv2.getTrackbarPos("DMODE", "Trackbars") == 2:
                display_mode = 2
    except:
        s('cls')
        print('\n\n     Debug menu: Off ')



    cv2.imshow('Fire Detection', curr_frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('0'):
        display_mode = 0
    elif key & 0xFF == ord('1'):
        display_mode = 1
    elif key & 0xFF == ord('2'):
        display_mode = 2
    elif key & 0xFF == ord('3'):
        show_direction = not show_direction
    elif key & 0xFF == ord('9'):
        dbg = not dbg
    elif key & 0xFF == ord('8'):
        Debug_menu()
        print('     Debug menu: On')


cv2.destroyAllWindows()
