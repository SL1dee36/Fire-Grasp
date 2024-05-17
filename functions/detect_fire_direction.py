import cv2


def detect_fire_direction(frame, contours, prev_center):
    for i, contour in enumerate(contours):
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if i in prev_center:
                deltaX = cX - prev_center[i][0]
                deltaY = cY - prev_center[i][1]
                directionX = "Right" if deltaX > 2 else "Left" if deltaX < -2 else ""
                directionY = "Down" if deltaY > 2 else "Up" if deltaY < -2 else ""
                direction = directionX + " " + directionY
                _, _, w, h = cv2.boundingRect(contour)
                if w > 150 and h > 150:
                    cv2.putText(frame, direction, (cX, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            prev_center[i] = [cX, cY]
    return frame
