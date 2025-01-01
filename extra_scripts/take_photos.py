"""
This script is used to take photos from the camera and save them to the specified path.
"""

from src.sensor.computer_camera import ComputerCamera

path = 'data/images/samples/'


def main():
    """ main function """
    camera = ComputerCamera()
    camera.initialize()
    camera.stream_video()


if __name__ == '__main__':
    main()
