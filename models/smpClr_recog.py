# Extremely Simple and basic color recognition

import cv2
import numpy as np

img = cv2.imread("../test_image/color_wheel.jpg")

# you can declare set boundaries of colors in a list or tuple, not doing that here
# opencv uses BGR, OpenCV represents images as NumPy arrays in reverse

# creates numpy arrays using high and low
# substitute whatever color you want
lower = np.array([0, 0, 0], dtype=None)
upper = np.array([255, 50, 50], dtype=None)

# most wide used color spaces are gray and hsv
# see difference in README.md
mask = cv2.inRange(img, lower, upper)
output = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("images", np.hstack([img, output]))

cv2.waitKey(0)
