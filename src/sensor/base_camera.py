"""
camera.py
"""

from abc import abstractmethod
from src.sensor.base_sensor import BaseSensor, SensorException


class CameraException(SensorException):
    """
    Camera Exception
    """


class BaseCamera(BaseSensor):
    """
    Base interface for all camera types.

    Defines the common methods that all camera implementations must provide.

    """

    @abstractmethod
    def initialize(self):
        """
        Initializes the camera.
        """

    @abstractmethod
    def capture_image(self):
        """
        Captures an image from the camera.

        Returns:
            str: The filename of the captured image.
        """

    @abstractmethod
    def release(self):
        """
        Releases the camera resources when done.
        """

    @abstractmethod
    def show_live_video(self):
        """
        Displays the live video feed from the computer's webcam until
        a key is pressed.
        """
