"""
rpi_camera.py
"""

# import time

from pathlib import Path
import cv2
from cv2.typing import MatLike

import numpy as np
from picamera2 import Picamera2

from src.sensor.base_camera import BaseCamera, CameraException

from src.utils import obtain_filenames_last_number


class RPiCameraException(CameraException):
    """
    RPi Camera Exception
    """


class RPiCamera(BaseCamera):
    """
    Camera implementation for the rpi's cam using OpenCV.
    """

    def __init__(self, name: str = "RPi Camera",
                 save_photos_path: Path = Path("data/images/samples"), photo_name: str = 'rpi_photo'):
        """
        Initializes the camera object to None.
        """
        self._name = name
        self._camera = None
        self.__save_photos_path = save_photos_path
        self.__photo_name = photo_name
        self.__photo_counter = obtain_filenames_last_number(self.__save_photos_path, self.__photo_name)

    def _is_init(self) -> bool:
        """
        Is camera init

        Returns:
            bool
        """
        if self._camera:
            return True
        print("Camera not initialized.")
        return False

    def calibrate(self):
        """
        Calibrate the sensor
        """

    def get_status(self):
        """
        Get the status of the sensor
        """

    def initialize(self):
        """
        Initializes the rpi's webcam using OpenCV.

        Raises an exception if the camera cannot be opened.
        """
        self._camera = Picamera2()
        # video resolution (optional)
        # self._camera.sensor_resolution = (1280, 720)
        if not self._camera:
            raise RPiCameraException("Error opening rpi webcam.")
        print("RPi webcam initialized.")

    def read(self) -> MatLike:
        """
        Read a value from the sensor
        """
        if not self._is_init():
            return
        # Crear una imagen en memoria (numpy array)
        image = self._camera.capture_image()
        return image

    def stream_video(self):
        """
        Displays the live video feed from the rpi's webcam.

        Options:
            - Press 'q' to quit
            - Press 's' | 'S' | ' ' to save a photo
        """
        if not self._is_init():
            return
        print("Press 'q' key to stop the live video feed.")
        while True:
            frame = self.read()
            cv2.imshow(f'{self._name} live streaming', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # ASCII code for 'q'
                # quit
                break
            if key == 32 or key == ord('s') or key == ord('S'):  # Space key or 's' key
                # save photo
                self.__photo_counter += 1
                photo_filename = self.__save_photos_path / f"{self.__photo_name}_{self.__photo_counter}.png"
                cv2.imwrite(photo_filename, frame)
                print(f"Photo saved as {photo_filename}")
        cv2.destroyAllWindows()

    def release(self):
        """
        Releases the camera resources when done.
        """
        if self._camera:
            self._camera.close()
            self._camera = None
            print(f"RPi Camera ({self._name}) released.")
