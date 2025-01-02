"""
computer_camera.py
"""

# import time

from pathlib import Path
import numpy as np
import cv2

from src.sensor.base_camera import BaseCamera, CameraException
from src.sensor.sensor_type import SensorType


class ComputerCameraException(CameraException):
    """
    Computer Camera Exception
    """


class ComputerCamera(BaseCamera):
    """
    Camera implementation for the computer's webcam using OpenCV.

    Attributes:
        _name (str): The name of the camera.
        _camera_id (int): The camera ID.
        _type (SensorType): The type of the camera.
        _status (str): The status of the camera.
        _camera (Any): The camera object.
        __photo_counter (int): The photo counter for saving photos.
        __save_photos_path (Path): The path to save photos.
        __photo_name (str): The name

    Methods:
        calibrate(): Calibrate the sensor
        get_status(): Get the status of the sensor
        initialize(): Initializes the camera
        read(): Captures an image from the camera
        stream_video(): Displays the live video feed from the camera
        release(): Releases the camera resources when done
    """

    def __init__(self, name: str = "Computer Camera",
                 save_photos_path: Path = Path("data/images/samples"), photo_name: str = 'photo'):
        """
        Initializes the camera object to None.

        Args:
            name (str): The name of the camera.
            save_photos_path (Path): The path to save photos.
            photo_name (str): The name of the photo.
        """
        super().__init__(name, s_type=SensorType.COMPUTER_CAMERA,
                         save_photos_path=save_photos_path, photo_name=photo_name)

    # ----- protected methods

    # ----- public methods

    def initialize(self) -> None:
        """
        Initializes the computer's webcam using OpenCV.

        Raises an exception if the camera cannot be opened.
        """
        self._camera = cv2.VideoCapture(0)  # 0 is the default webcam index
        if not self._camera.isOpened():
            raise ComputerCameraException("Error opening computer webcam.")
        print("Computer webcam initialized.")

    def read(self) -> np.ndarray:
        """
        Read a value from the camera.

        Returns:
            np.ndarray: The image captured from the camera.
        """
        # if not self._is_init():
        #     return
        ret, frame = self._camera.read()
        if not ret:
            raise ComputerCameraException("Failed to grab frame.")
        return frame

    def stream_video(self) -> None:
        """
        Displays the live video feed from the computer's webcam.

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

    def release(self) -> None:
        """
        Releases the camera resources when done.
        """
        if self._camera:
            self._camera.release()
            self._camera = None
            print(f"Computer Camera ({self._name}) released.")
