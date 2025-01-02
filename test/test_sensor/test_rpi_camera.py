"""
test_rpi_camera.py
"""


from src.sensor.rpi_camera import RPiCamera, RPiCameraException


def test_initialize_camera(ccamera: RPiCamera) -> None:
    """
    test
    """
    try:
        ccamera.initialize()
        print('YES')
    except RPiCameraException:
        print('NO')


def test_capture_image(ccamera: RPiCamera) -> None:
    """
    test
    """
    frame = ccamera.read()
    if frame is not None:
        print('YES')
    else:
        print('NO')


def test_live_video(ccamera: RPiCamera) -> None:
    """
    test
    """
    try:
        ccamera.stream_video()
        print('YES')
    except RPiCameraException:
        print('NO')


def test_release_camera(ccamera: RPiCamera) -> None:
    """
    test
    """
    try:
        ccamera.release()
        print('YES')
    except RPiCameraException:
        print('NO')


def main():
    """
    main
    """
    ccamera = RPiCamera()
    test_initialize_camera(ccamera)
    test_capture_image(ccamera)
    test_live_video(ccamera)
    test_release_camera(ccamera)


if __name__ == '__main__':
    main()
