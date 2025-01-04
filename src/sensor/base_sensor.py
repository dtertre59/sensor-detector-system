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
        calibrate() -> None: Calibrate the sensor
        read() -> Any: Read a value from the sensor
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The name of the sensor
        """

    @property
    @abstractmethod
    def type(self) -> SensorType:
        """
        The type of the sensor
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
