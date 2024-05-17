import cv2
import numpy as np

def Debug_menu():
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 500, 400)
    for i in ["LOW", "HIGH"]:
        for j in range(3):
            param = f"{i}_{j}"
            if i == "LOW":
                v = 0
            else:
                v = 255
            cv2.createTrackbar(param, "Trackbars", v, 255, lambda x: None)
    cv2.createTrackbar("RESET", "Trackbars", 0, 1, lambda x: None)
    cv2.createTrackbar("PRINT", "Trackbars", 0, 1, lambda x: None)
    cv2.createTrackbar("DMODE", "Trackbars", 0, 2, lambda x: None)
    #cv2.createTrackbar("resolution", "Trackbars", 0, 4, lambda x: None)
