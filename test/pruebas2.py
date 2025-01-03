import time
from pathlib import Path
import numpy as np
import cv2
from picamera2 import Picamera2
from src.utils import show_image

camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": "XRGB8888", "size": (640, 480)}))
camera.start()
time.sleep(1)
while True:
    frame = camera.capture_array()
    # frame = np.array(frame, dtype=np.uint8)
    cv2.imshow("camera", frame)
    print(1)
    cv2.waitKey(0)
    # cv2.imwrite('bb.jpg', frame)
    # camera.stop()
    # time.sleep(2)
    # image = cv2.imread('bb.jpg')
    # print(image)
    # show_image(image)

# print(type(frame))
# print(frame.shape)
# show_image(frame)
