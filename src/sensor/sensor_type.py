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


if __name__ == "__main__":
    print(SensorType.COMPUTER_CAMERA)
    print(repr(SensorType.COMPUTER_CAMERA))
    print(str(SensorType.COMPUTER_CAMERA))
    print(SensorType.COMPUTER_CAMERA.name)
    print(SensorType.COMPUTER_CAMERA.value)
    print(SensorType.COMPUTER_CAMERA == SensorType.COMPUTER_CAMERA)
    print(SensorType.COMPUTER_CAMERA == SensorType.RPI_CAMERA)
    print(SensorType.COMPUTER_CAMERA == "computer_camera")
    print(SensorType.COMPUTER_CAMERA == SensorType("computer_camera"))

    print(SensorType("computer_camera"))
