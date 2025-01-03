import time
from pathlib import Path
import numpy as np
import cv2
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from src.utils import show_image

camera = Picamera2()
video_config = camera.create_video_configuration()
camera.configure(video_config)

encoder = H264Encoder(10000000)
camera.start_recording(encoder, 'test.mp4')
# time.sleep(1)
# frame = camera.capture_array()
# frame = np.array(frame, dtype=np.uint8)
# cv2.imwrite('bb.jpg', frame)
# camera.stop()
time.sleep(3)
camera.stop_recording()
# image = cv2.imread('bb.jpg')
# print(image)
# show_image(image)

# camera.capture_file('ccc.png')

# print(type(frame))
# print(frame.shape)
# show_image(frame)
