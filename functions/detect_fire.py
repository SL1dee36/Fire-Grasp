import cv2
import numpy as np
from functions.draw_hexagon import draw_hexagon

KERNEL_SIZE = (3, 3)
DILATE_ITERATIONS = 3
ERODE_ITERATIONS = 2

OUTLINE_INDEX_MAP = {
    0: "SURFACE AREA",
    1: "RECTANGLE",
    2: "HEXAGON",
}


def _normalize_outline_type(outline_type):
    if isinstance(outline_type, int):
        return OUTLINE_INDEX_MAP.get(outline_type, "SURFACE AREA")
    return str(outline_type).upper()


def _read_trackbar_bounds(lower_bound, upper_bound):
    try:
        l_h = cv2.getTrackbarPos("LOW_0", "Trackbars")
        l_s = cv2.getTrackbarPos("LOW_1", "Trackbars")
        l_v = cv2.getTrackbarPos("LOW_2", "Trackbars")
        h_h = cv2.getTrackbarPos("HIGH_0", "Trackbars")
        h_s = cv2.getTrackbarPos("HIGH_1", "Trackbars")
        h_v = cv2.getTrackbarPos("HIGH_2", "Trackbars")
        if min(l_h, l_s, l_v, h_h, h_s, h_v) < 0:
            return lower_bound, upper_bound
        return (l_h, l_s, l_v), (h_h, h_s, h_v)
    except cv2.error:
        return lower_bound, upper_bound


def detect_fire(
    frame,
    dbg,
    outline_type,
    hexagon_size,
    lower_bound,
    upper_bound,
    dilate_iter,
    erode_iter,
    kernel_size=KERNEL_SIZE,
):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if dbg:
        lower_bound, upper_bound = _read_trackbar_bounds(lower_bound, upper_bound)

    lower_fire = np.array(lower_bound, dtype=np.uint8)
    upper_fire = np.array(upper_bound, dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_fire, upper_fire)

    kernel = np.ones(kernel_size, np.uint8)
    if dilate_iter > 0:
        mask = cv2.dilate(mask, kernel, iterations=int(dilate_iter))
    if erode_iter > 0:
        mask = cv2.erode(mask, kernel, iterations=int(erode_iter))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if not contours:
        return frame, contours

    centers = np.array(
        [
            (x + w // 2, y + h // 2)
            for x, y, w, h in (cv2.boundingRect(c) for c in contours)
        ],
        dtype=np.float32,
    )

    mode = _normalize_outline_type(outline_type)
    min_area = hexagon_size * hexagon_size

    for i, contour in enumerate(contours):
        if cv2.contourArea(contour) <= min_area:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        center = (int(centers[i][0]), int(centers[i][1]))
        max_len = max(w, h)

        # Merge very close neighbor contour into the next contour if within threshold
        if len(contours) > 1:
            dists = np.linalg.norm(centers - centers[i], axis=1)
            dists[i] = np.inf
            nearest_idx = int(np.argmin(dists))
            if dists[nearest_idx] < max_len / 9:
                contours[nearest_idx] = np.concatenate((contour, contours[nearest_idx]))

        if mode == "RECTANGLE":
            if any(cv2.pointPolygonTest(big_c, center, False) > 0 for big_c in contours[:i]):
                continue
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        elif mode == "HEXAGON":
            moments = cv2.moments(contour)
            if moments["m00"] != 0:
                c_x = int(moments["m10"] / moments["m00"])
                c_y = int(moments["m01"] / moments["m00"])
                draw_hexagon(frame, (c_x, c_y), hexagon_size, (0, 255, 0))
        elif mode in ("SURFACE AREA", "SA"):
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

    return frame, contours
