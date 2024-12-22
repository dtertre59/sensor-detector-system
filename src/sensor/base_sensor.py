"""
BaseSensor class is an abstract class that defines the methods
that all sensors should implement.
"""

from abc import ABC, abstractmethod


class SensorException(Exception):
    """
    Base exception for all sensor-related errors.
    """


class BaseSensor(ABC):
    """
        Abstract base class for sensors
    """

    @abstractmethod
    def read_value(self):
        """
        Read a value from the sensor
        """

    @abstractmethod
    def calibrate(self):
        """
        Calibrate the sensor
        """

    @abstractmethod
    def get_status(self):
        """
        Get the status of the sensor
        """
