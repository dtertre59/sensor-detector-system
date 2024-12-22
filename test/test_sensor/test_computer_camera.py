"""
test_computer_camera.py
"""


from src.sensor.computer_camera import ComputerCamera, ComputerCameraException


def test_initialize_camera(ccamera: ComputerCamera) -> None:
    """
    test
    """
    try:
        result = ccamera.initialize()
        if result:
            print('YES')
    except ComputerCameraException:
        print('NO')


def test_capture_image(ccamera: ComputerCamera) -> None:
    """
    test
    """
    frame, filename = ccamera.capture_image()
    if frame is not None:
        print('YES')
    else:
        print('NO')
    if filename:
        print('YES')
    else:
        print('NO')


def test_live_video(ccamera: ComputerCamera) -> None:
    """
    test
    """
    ccamera.show_live_video()


def main():
    """
    main
    """
    ccamera = ComputerCamera()
    test_initialize_camera(ccamera)
    # test_capture_image(ccamera)
    test_live_video(ccamera)


if __name__ == '__main__':
    main()
