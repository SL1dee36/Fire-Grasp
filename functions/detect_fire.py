import cv2
import numpy as np
from functions.draw_hexagon import draw_hexagon
from scipy.spatial import distance, KDTree

KERNEL_SIZE = (1, 1)
DILATE_ITERATIONS = 10
ERODE_ITERATIONS = 50

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
        l_h,l_s,l_v = 0,100,255
        h_h,h_s,h_v = 25,255,255

    lower_fire = np.array([l_h, l_s, l_v])
    upper_fire = np.array([h_h, h_s, h_v])
    mask = cv2.inRange(hsv, lower_fire, upper_fire)
    kernel = np.ones(KERNEL_SIZE, np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=DILATE_ITERATIONS)
    mask = cv2.erode(mask, kernel, iterations=ERODE_ITERATIONS)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)  # Sorting contours by area

    centers = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        center = (x + w//2, y + h//2)
        centers.append(center)
    try:
        tree = KDTree(centers)
    except: pass #Skip if no trees were detected to avoid an error and a crash.
        
    for i, contour in enumerate(contours):
        if cv2.contourArea(contour) > hexagon_size * hexagon_size:
            x, y, w, h = cv2.boundingRect(contour)
            center = (x + w//2, y + h//2)
            max_len = max(w, h)  #

            # Combining circuits
            dists, inds = tree.query(center, 2)  # Request for two immediate neighbors
            for dist, j in zip(dists[1:], inds[1:]):  # Ignoring the first neighbor, i.e., yourself
                if dist < max_len // 9:
                    contours[j] = np.concatenate((contour, contours[j]))

            if display_mode == 1:
                for big_contour in contours:
                    if cv2.pointPolygonTest(big_contour, center, False) > 0:
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
