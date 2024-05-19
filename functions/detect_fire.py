import cv2
import numpy as np
from functions.draw_hexagon import draw_hexagon

def detect_fire(frame, dbg, display_mode, hexagon_size):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    try:
        if dbg == True:
            l_h = cv2.getTrackbarPos("LOW_0", "Trackbars")
            l_s = cv2.getTrackbarPos("LOW_1", "Trackbars")
            l_v = cv2.getTrackbarPos("LOW_2", "Trackbars")
            h_h = cv2.getTrackbarPos("HIGH_0", "Trackbars")
            h_s = cv2.getTrackbarPos("HIGH_1", "Trackbars")
            h_v = cv2.getTrackbarPos("HIGH_2", "Trackbars")
    except:
        l_h = 0
        l_s = 100
        l_v = 255
        h_h = 25
        h_s = 255
        h_v = 255

    lower_fire = np.array([l_h, l_s, l_v])
    upper_fire = np.array([h_h, h_s, h_v])
    mask = cv2.inRange(hsv, lower_fire, upper_fire)
    kernel = np.ones((1, 1), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=10)
    mask = cv2.erode(mask, kernel, iterations=50)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > hexagon_size * hexagon_size:
            x, y, w, h = cv2.boundingRect(contour)
            # Если мы дошли до этого места, значит, маленький квадрат не находится внутри большого
            if display_mode == 1:
                # Проверяем, находится ли центр маленького квадрата внутри большого
                center = (x + w//2, y + h//2)
                for big_contour in contours:
                    if cv2.pointPolygonTest(big_contour, center, False) > 0:
                        # Если центр маленького квадрата находится внутри большого, пропускаем его
                        continue

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            elif display_mode == 2:
                M = cv2.moments(contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                draw_hexagon(frame, (cX, cY), hexagon_size, (0, 255, 0))

            elif display_mode == 0:
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
    return frame, contours
