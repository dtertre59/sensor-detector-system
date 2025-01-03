"""
rpi_camera.py
"""

import platform
from pathlib import Path
import numpy as np
import cv2

from src.sensor.base_camera import BaseCamera, CameraException
from src.sensor.sensor_type import SensorType

# Check if the operating system is Linux
if platform.system() != "Linux":
    raise EnvironmentError("RPiCamera is only supported on Linux.")
else:
    from picamera2 import Picamera2  # pylint: disable=import-error  # type: ignore


class RPiCameraException(CameraException):
    """
    RPi Camera Exception
    """


class RPiCamera(BaseCamera):
    """
    Camera implementation for the rpi's cam using OpenCV.

    Attributes:
        _name (str): The name of the camera.
        _camera_id (int): The camera ID.
        _type (SensorType): The type of the camera.
        _status (str): The status of the camera.
        _camera (Any): The camera object.
        __photo_counter (int): The photo counter for saving photos.
        __save_photos_path (Path): The path to save photos.
        __photo_name (str): The name

    Methods:
        calibrate(): Calibrate the sensor
        get_status(): Get the status of the sensor
        initialize(): Initializes the camera
        read(): Captures an image from the camera
        stream_video(): Displays the live video feed from the camera
        release(): Releases the camera resources when done
    """

    def __init__(self, name: str = "RPi Camera",
                 save_photos_path: Path = Path("data/images/samples"), photo_name: str = 'rpi_photo'):
        """
        Initializes the camera object to None.
        """
        super().__init__(name, s_type=SensorType.RPI_CAMERA,
                         save_photos_path=save_photos_path, photo_name=photo_name)

    # ----- protected methods

    # ----- public methods

    def initialize(self) -> None:
        """
        Initializes the rpi's webcam using OpenCV.

        Raises:
            RPiCameraException: If there is an error opening the rpi's cam.
        """
        self._camera = Picamera2()
        self._camera.configure(self._camera.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
        self._camera.start()

        if not self._camera:
            raise RPiCameraException("Error opening rpi cam.")
        print("RPi webcam initialized.")

    def read(self) -> np.ndarray:
        """
        Read a value from the rpi's camera.

        Returns:
            np.ndarray: The image frame from the camera.
        """
        # if not self._is_init():
        #     return
        frame = self._camera.capture_array()
        frame = np.array(frame, dtype=np.uint8)
        print('goof read')
        cv2.imwrite('aaa1.jpg', frame)
        return frame

    def stream_video(self) -> None:
        """
        Displays the live video feed from the rpi's cam.

        Options:
            - Press 'q' to quit
            - Press 's' | 'S' | ' ' to save a photo
        """
        if not self._is_init():
            return
        print("Press 'q' key to stop the live video feed.")
        while True:
            frame = self.read()
            cv2.imshow(f'{self._name} live streaming', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # ASCII code for 'q'
                # quit
                break
            if key == 32 or key == ord('s') or key == ord('S'):  # Space key or 's' key
                # save photo
                self.__photo_counter += 1
                photo_filename = self.__save_photos_path / f"{self.__photo_name}_{self.__photo_counter}.png"
                cv2.imwrite(photo_filename, frame)
                print(f"Photo saved as {photo_filename}")
        cv2.destroyAllWindows()

    def release(self):
        """
        Releases the camera resources when done.
        """
        if self._camera:
            self._camera.close()
            self._camera = None
            print(f"RPi Camera ({self._name}) released.")
