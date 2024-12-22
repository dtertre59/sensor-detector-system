"""
detector.py
"""

from abc import ABC, abstractmethod


class DetectorException(Exception):
    """
    Detector Exception
    """


class BaseDetector(ABC):
    """
    Abstract base class for detectors.
    """

    @abstractmethod
    def initialize(self):
        """
        Initializes the detector.
        """

    @abstractmethod
    def detect(self, image):
        """
        Detects objects or patterns in the provided image.

        Args:
            image (numpy.ndarray): The image from the camera.

        Returns:
            bool: True if an object is detected, False otherwise.
        """

    @abstractmethod
    def process_detection(self, detection_result):
        """
        Processes the result of a detection.

        Args:
            detection_result (dict): A dictionary containing the detection result.
        """

    @abstractmethod
    def reset(self):
        """
        Resets the detector, clearing any internal states or buffers.
        """

    @abstractmethod
    def get_status(self):
        """
        Returns the current status of the detector (e.g., whether it's active or idle).

        Returns:
            str: The status of the detector.
        """
