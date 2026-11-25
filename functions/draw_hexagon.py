import math
import cv2
import numpy as np


def draw_hexagon(img, center_coordinates, size, color):
    w = math.sqrt(3) / 2 * size
    h = size
    cx, cy = center_coordinates
    points = np.array(
        [
            [cx, cy - h],
            [cx + w, cy - h / 2],
            [cx + w, cy + h / 2],
            [cx, cy + h],
            [cx - w, cy + h / 2],
            [cx - w, cy - h / 2],
        ],
        dtype=np.float32,
    )
    cv2.polylines(img, [np.round(points).astype(np.int32)], True, color, 2)
