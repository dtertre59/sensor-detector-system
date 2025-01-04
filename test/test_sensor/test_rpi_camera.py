"""
test_rpi_camera.py
"""


from src.sensor.rpi_camera import RPiCamera, RPiCameraException
from src.utils import show_image


def test_initialize_camera(rpi_camera: RPiCamera) -> None:
    """
    test
    """
    try:
        rpi_camera.initialize()
        print('YES')
    except RPiCameraException:
        print('NO')


def test_capture_image(rpi_camera: RPiCamera) -> None:
    """
    test
    """
    frame = rpi_camera.read()
    show_image(frame)
    if frame is not None:
        print('YES')
    else:
        print('NO')


def test_live_video(rpi_camera: RPiCamera) -> None:
    """
    test
    """
    try:
        rpi_camera.stream_video()
        print('YES')
    except RPiCameraException:
        print('NO')


def test_release_camera(rpi_camera: RPiCamera) -> None:
    """
    test
    """
    try:
        rpi_camera.release()
        print('YES')
    except RPiCameraException:
        print('NO')


def main():
    """
    main
    """
    rpi_camera = RPiCamera()
    test_initialize_camera(rpi_camera)
    print(rpi_camera._camera)
    test_capture_image(rpi_camera)
    test_live_video(rpi_camera)
    test_release_camera(rpi_camera)


if __name__ == '__main__':
    main()
