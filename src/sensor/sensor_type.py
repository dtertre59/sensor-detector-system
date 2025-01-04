"""
SensorType is an enumeration of the different types of sensors that can be.
"""

from enum import Enum


class SensorType(Enum):
    """
    SensorType is an enumeration of the different types of sensors that can be
    used in the system. This is used to specify the type of sensor that is
    being used in the system.
    """
    CAMERA = "camera"
    COMPUTER_CAMERA = "computer_camera"
    RPI_CAMERA = "rpi_camera"
    DENSITY_SENSOR = "density_sensor"
