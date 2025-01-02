"""
BaseSensor class is an abstract class that defines the methods
that all sensors should implement.
"""

from abc import ABC, abstractmethod
from typing import Any
from src.sensor.sensor_type import SensorType


class SensorException(Exception):
    """
    Base exception for all sensor-related errors.
    """


class BaseSensor(ABC):
    """
    Abstract base class for sensors.
    Defines the common methods that all sensor implementations must provide.

    Methods:
        get_type() -> SensorType: Get the type of the sensor
        get_status() -> str: Get the status of the sensor
        calibrate() -> None: Calibrate the sensor
        read() -> Any: Read a value from the sensor
    """

    @abstractmethod
    def get_type(self) -> SensorType:
        """
        Get the type of the sensor

        Returns:
            SensorType: The type of the sensor
        """

    @abstractmethod
    def get_status(self) -> str:
        """
        Get the status of the sensor

        Returns:
            str: The status of the sensor
        """

    @abstractmethod
    def calibrate(self) -> None:
        """
        Calibrate the sensor
        """

    @abstractmethod
    def read(self) -> Any:
        """
        Read a value from the sensor

        Returns:
            Any: The value read from the sensor
        """
