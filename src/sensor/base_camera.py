"""
camera.py
"""

from pathlib import Path
import numpy as np

from src.sensor.base_sensor import BaseSensor, SensorException
from src.sensor.sensor_type import SensorType

from src.utils import obtain_filenames_last_number


class CameraException(SensorException):
    """
    Camera Exception
    """


class BaseCamera(BaseSensor):
    """
    Base interface for all camera types.
    Defines the common methods that all camera implementations must provide.

    Attributes:
        _name (str): The name of the camera.
        _camera_id (int): The camera ID.
        _type (SensorType): The type of the camera.
        _status (str): The status of the camera.
        _camera (Any): The camera object.
        __save_photos_path (Path): The path to save photos.
        __photo_name (str): The name of the photo.
        __photo_counter (int): The photo counter for saving photos.

    Methods:
        get_type() -> SensorType: Get the type of the camera
        get_status() -> str: Get the status of the camera
        calibrate() -> None: Calibrate the camera
        initialize(): Initializes the camera
        read() -> str: Captures an image from the camera
        stream_video(): Displays the live video feed from the camera
        release(): Releases the camera resources when done
    """

    def __init__(self, name: str = "Camera", camera_id: int = 0, s_type: SensorType = SensorType.CAMERA,
                 save_photos_path: Path = Path("data/images/samples"), photo_name: str = 'photo'):
        """
        Initializes the camera object to None.

        Args:
            name (str): The name of the camera.
            camera_id (int): The camera ID.
            s_type (SensorType): The type of the camera.
            save_photos_path (Path): The path to save photos.
            photo_name (str): The name of the photo.
        """
        self._name = name
        self._camera_id = camera_id
        self._type = s_type
        self._status = "idle"

        self._camera = None

        self.__save_photos_path = save_photos_path
        self.__photo_name = photo_name
        self.__photo_counter = obtain_filenames_last_number(self.__save_photos_path, self.__photo_name)
    
    # ----- properties and setters
    
    @property
    def save_photos_path(self, path: Path) -> None:
        """
        """
    
    # ----- protected methods

    def _is_init(self) -> bool:
        """
        Is camera init.

        Returns:
            bool
        """
        if self._camera:
            return True
        print("Camera not initialized.")
        return False

    # ----- public methods

    def get_type(self) -> SensorType:
        """
        Get the type of the camera

        Returns:
            SensorType: The type of the sensor
        """
        return self._type

    def get_status(self) -> str:
        """
        Get the status of the camera

        Returns:
            str: The status of the camera
        """
        return self._status

    def get_photo_counter(self) -> int:
        """
        Get the photo counter

        Returns:
            int: The photo counter
        """
        return self.__photo_counter
    
    def update_photo_counter(self, n: int = 1) -> None:
        """
        Update the photo counter
        
        Args:
            n (int): counter increment
        """
        self.__photo_counter += 1

    # ----- Not implemented in the base class

    def calibrate(self) -> None:
        """
        Calibrate the camera
        """

    def initialize(self) -> None:
        """
        Initializes the camera.
        """

    def read(self) -> np.ndarray:
        """
        Captures an image from the camera.

        Returns:
            np.ndarray: The image captured from the camera.
        """

    def stream_video(self) -> None:
        """
        Displays the live video feed from the computer's webcam until
        a key is pressed.
        """

    def release(self) -> None:
        """
        Releases the camera resources when done.
        """
