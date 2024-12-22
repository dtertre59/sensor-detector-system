"""
utils.py
"""

import cv2


def show_image(image):
    """
    show image
    """
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
