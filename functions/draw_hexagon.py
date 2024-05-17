import cv2
import math
import numpy as np

def draw_hexagon(img, center_coordinates, size, color):
    w = math.sqrt(3) / 2 * size
    h = size
    points = np.array([[center_coordinates[0], center_coordinates[1] - h],
                       [center_coordinates[0] + w, center_coordinates[1] - h / 2],
                       [center_coordinates[0] + w, center_coordinates[1] + h / 2],
                       [center_coordinates[0], center_coordinates[1] + h],
                       [center_coordinates[0] - w, center_coordinates[1] + h / 2],
                       [center_coordinates[0] - w, center_coordinates[1] - h / 2]], np.int32)
    cv2.polylines(img, [points], True, color, 2)
