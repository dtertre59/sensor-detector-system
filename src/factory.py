"""
Factory classes.
"""

import platform
from abc import ABC, abstractmethod
from typing import Any

from enum import Enum

from src.sensor.sensor_type import SensorType
from src.sensor.base_sensor import BaseSensor
from src.sensor.computer_camera import ComputerCamera

from src.detector.detector_type import DetectorType
from src.detector.base_detector import BaseDetector
from src.detector.color_detector import ColorDetector

if platform.system() == "Linux":
    from src.sensor.rpi_camera import RPiCamera


class Factory(ABC):
    """
    Abstract base class for factories.

    Methods:
        create(object_type: Enum) -> Any: Create a new instance of a product.
    """

    @abstractmethod
    def create(self, object_type: Enum) -> Any:
        """
        Create a new instance of a product.

        Args:
            object_type (Enum): The type of object to create.

        Returns:
            Any: The created product instance.
        """


class SensorFactory(Factory):
    """
    Factory class for creating sensor objects.

    Methods:
        create(object_type: SensorType) -> BaseSensor: Create a new sensor object.
    """

    def create(self, object_type: SensorType) -> BaseSensor:
        """
        Create a new sensor object.

        Args:
            object_type (SensorType): The type of sensor to create

        Returns:
            Any: The created sensor object.
        """
        if object_type == SensorType.COMPUTER_CAMERA:
            return ComputerCamera()
        elif object_type == SensorType.RPI_CAMERA and platform.system() == "Linux":
            return RPiCamera()  # pylint: disable=E0606
        else:
            raise ValueError(f"Invalid sensor type: {object_type.name}")


class DetectorFactory(Factory):
    """
    Factory class for creating detector objects.

    Methods:
        create(object_type: DetectorType) -> BaseDetector: Create a new detector object.
    """

    def create(self, object_type: DetectorType) -> BaseDetector:
        """
        Create a new detector object.

        Returns:
            Any: The created detector object.
        """
        if object_type == DetectorType.COLOR_DETECTOR:
            return ColorDetector()
        else:
            raise ValueError(f"Invalid detector type: {object_type.name}")
