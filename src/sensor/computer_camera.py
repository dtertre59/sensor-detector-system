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
        _photo_path (Path): The path to save photos.
        _photo_name (str): The name of the photo.
        _photo_counter (int): The photo counter for saving photos.
        _video_path (Path): The path to save videos.
        _video_name (str): The name of the video.
        _video_counter (int): The video counter for saving videos.
        _camera (Any): The camera object.
        _camera_config (Any): The camera configuration object.

    Methods:
        _is_init(): Is camera init.
        _save_photo(frame: np.ndarray, verbose: bool = False): Save a photo from the camera.
        _increment_photo_counter(value: int = 1): Update the photo counter
        calibrate(): Calibrate the sensor
        initialize(): Initializes the camera
        read(): Captures an image from the camera
        stream_video(): Displays the live video feed from the camera
        record_video(): Record a video from the camera
        release(): Releases the camera resources when done
    """

    def __init__(self, name: str = "Computer Camera",
                 photo_path: Path = Path("data/images/samples"), photo_name: str = 'photo',
                 video_path: Path = Path("data/videos/samples"), video_name: str = 'video'):
        """
        Initializes the camera object to None.

        Args:
            name (str): The name of the camera.
            photo_path (Path): The path to save photos.
            photo_name (str): The name of the photo.
            video_path (Path): The path to save videos.
            video_name (str): The name of the video.
        """
        super().__init__(name, s_type=SensorType.COMPUTER_CAMERA,
                         photo_path=photo_path, photo_name=photo_name,
                         video_path=video_path, video_name=video_name)

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
        frame = cv2.resize(frame, self._resolution)
        if not ret:
            raise ComputerCameraException("Failed to grab frame.")
        return frame

    def release(self) -> None:
        """
        Releases the camera resources when done.
        """
        if self._camera:
            self._camera.release()
            self._camera = None
            print(f"Computer Camera ({self._name}) released.")
