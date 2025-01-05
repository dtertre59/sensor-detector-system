"""
test_camera_fps.py
"""

import time
import platform
from src.sensor.computer_camera import ComputerCamera

if platform.system() == 'Linux':
    from src.sensor.rpi_camera import RPiCamera


def test_computer_camera():
    """
    test
    """
    camera = ComputerCamera()
    camera.initialize()
    start_time = time.time()
    num_frames = 100
    for _ in range(num_frames):
        print('a')
        _ = camera.read()
    elapsed_time = time.time() - start_time
    print(f"FPS: {num_frames / elapsed_time:.2f}")


def test_rpi_camera():
    """
    test
    """
    camera = RPiCamera()
    camera.initialize()
    start_time = time.time()
    num_frames = 100
    for _ in range(num_frames):
        _ = camera.read()
    elapsed_time = time.time() - start_time
    print(f"FPS: {num_frames / elapsed_time:.2f}")


def main():
    """
    main
    """
    test_computer_camera()


if __name__ == '__main__':
    main()
