"""
This script is used to take photos from the camera and save them to the specified path.
"""

from src.factory import SensorFactory
from src.sensor.sensor_type import SensorType
from src.sensor.base_camera import BaseCamera


def main():
    """
    main function
    """
    camera: BaseCamera = SensorFactory.create(SensorType.RPI_CAMERA)
    camera.video_name = 'full_video'
    camera.initialize()
    camera.stream_video(True)
    camera.release()


if __name__ == '__main__':
    main()
