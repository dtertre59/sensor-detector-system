"""
test_sensor_factory.py
"""

import platform
from src.factory import SensorFactory
from src.sensor.sensor_type import SensorType


def test_computer_camera_instance():
    """
    test
    """
    sensor = SensorFactory().create(SensorType.COMPUTER_CAMERA)
    if sensor.type == SensorType.COMPUTER_CAMERA:
        print('OK')
    else:
        print('NO')


def test_rpi_camera_instance():
    """
    test
    """
    if platform.system() == "Linux":
        sensor = SensorFactory().create(SensorType.RPI_CAMERA)
        if sensor.type() == SensorType.RPI_CAMERA:
            print('OK')
        else:
            print('NO')
    else:
        try:
            sensor = SensorFactory().create(SensorType.RPI_CAMERA)
        except ValueError as e:
            print('OK -----', e)


def main():
    """
    main
    """
    test_computer_camera_instance()
    test_rpi_camera_instance()


if __name__ == '__main__':
    main()
