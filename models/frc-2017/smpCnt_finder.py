import cv2
import numpy as np

"""
im2, contours, hierarchy = cv2.findContours(find_mask(final_image), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnt = max(contours, key=cv2.contourArea)
"""