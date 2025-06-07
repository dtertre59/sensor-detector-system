"""
This script is used to take photos from the camera and save them to the specified path.
"""

from pathlib import Path

from src.factory import SensorFactory
from src.sensor.sensor_type import SensorType
from src.sensor.base_camera import BaseCamera


def main():
    """
    main function
    """
    camera: BaseCamera = SensorFactory.create(SensorType.RPI_CAMERA)
    camera.video_name = 'full_video_tspeed3'
    camera.photo_name = 'pcb'
    camera.photo_path = Path('data/images/dataset_2/pcb')
    camera.initialize()
    camera.stream_video(show_fps=False, verbose=True)
    camera.release()


if __name__ == '__main__':
    main()
