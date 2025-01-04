"""
test_computer_camera.py
"""


from src.sensor.computer_camera import ComputerCamera, ComputerCameraException


def test_initialize_camera(ccamera: ComputerCamera) -> None:
    """
    test
    """
    try:
        ccamera.initialize()
        print('YES')
    except ComputerCameraException:
        print('NO')


def test_capture_image(ccamera: ComputerCamera) -> None:
    """
    test
    """
    frame = ccamera.read()
    if frame is not None:
        print('YES')
    else:
        print('NO')


def test_live_video(ccamera: ComputerCamera) -> None:
    """
    test
    """
    try:
        ccamera.stream_video()
        print('YES')
    except ComputerCameraException:
        print('NO')


def test_release_camera(ccamera: ComputerCamera) -> None:
    """
    test
    """
    try:
        ccamera.release()
        print('YES')
    except ComputerCameraException:
        print('NO')


def test_video_recording(ccamera: ComputerCamera) -> None:
    """
    test
    """
    try:
        ccamera.record_video_standar()
        print('YES')
    except ComputerCameraException:
        print('NO') 


def main():
    """
    main
    """
    ccamera = ComputerCamera()
    test_initialize_camera(ccamera)
    # test_capture_image(ccamera)
    # test_live_video(ccamera)

    test_video_recording(ccamera)
    test_release_camera(ccamera)


if __name__ == '__main__':
    main()
