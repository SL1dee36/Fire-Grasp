import math
import cv2


def detect_fire_direction(frame, contours, prev_center):
    """Estimate movement direction for large fire contours by nearest-centroid matching."""
    new_centers = {}
    used_prev_keys = set()

    for idx, contour in enumerate(contours):
        moments = cv2.moments(contour)
        if moments["m00"] == 0:
            continue

        c_x = int(moments["m10"] / moments["m00"])
        c_y = int(moments["m01"] / moments["m00"])
        _, _, w, h = cv2.boundingRect(contour)
        max_match_dist = max(w, h, 80)

        best_key = None
        best_dist = max_match_dist
        for key, (p_x, p_y) in prev_center.items():
            if key in used_prev_keys:
                continue
            dist = math.hypot(c_x - p_x, c_y - p_y)
            if dist < best_dist:
                best_dist = dist
                best_key = key

        if best_key is not None:
            used_prev_keys.add(best_key)
            delta_x = c_x - prev_center[best_key][0]
            delta_y = c_y - prev_center[best_key][1]
            dir_x = "Right" if delta_x > 2 else "Left" if delta_x < -2 else ""
            dir_y = "Down" if delta_y > 2 else "Up" if delta_y < -2 else ""
            direction = f"{dir_x} {dir_y}".strip()
            if direction and w > 150 and h > 150:
                cv2.putText(
                    frame,
                    direction,
                    (c_x, max(25, c_y - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

        new_centers[idx] = [c_x, c_y]

    prev_center.clear()
    prev_center.update(new_centers)
    return frame
