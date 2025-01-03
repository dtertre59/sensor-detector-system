import cv2
import numpy as np
from src.utils import show_image

# image = np.zeros((300,300,3), dtype="uint8")
image = cv2.imread('aaa1.jpg')
print(image)
show_image(image)
