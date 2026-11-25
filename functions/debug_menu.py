import cv2


def Debug_menu(lower=(5, 65, 145), upper=(30, 255, 255), outline_idx=0):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 500, 550)
    for j in range(3):
        cv2.createTrackbar(f"LOW_{j}", "Trackbars", int(lower[j]), 255, lambda x: None)
    for j in range(3):
        cv2.createTrackbar(f"HIGH_{j}", "Trackbars", int(upper[j]), 255, lambda x: None)
    cv2.createTrackbar("RESET", "Trackbars", 0, 1, lambda x: None)
    cv2.createTrackbar("PRINT", "Trackbars", 0, 1, lambda x: None)
    cv2.createTrackbar("OUTLINE", "Trackbars", int(outline_idx), 2, lambda x: None)
