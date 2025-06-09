"""
rpi_camera.py
"""

import platform
import time
from pathlib import Path
import numpy as np
# import cv2

from src.sensor.base_camera import BaseCamera, CameraException
from src.sensor.sensor_type import SensorType

# Check if the operating system is Linux
if platform.system() != "Linux":
    raise EnvironmentError("RPiCamera is only supported on Linux.")
else:
    from picamera2 import Picamera2  # pylint: disable=import-error  # type: ignore
    from picamera2.encoders import H264Encoder, Quality


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
        _photo_path (Path): The path to save photos.
        _photo_name (str): The name of the photo.
        _photo_counter (int): The photo counter for saving photos.
        _video_path (Path): The path to save videos.
        _video_name (str): The name of the video.
        _video_counter (int): The video counter for saving videos.
        _camera (Any): The camera object.
        _camera_config (Any): The camera configuration object.

    Methods:
        _is_init(): Is camera init.
        _save_photo(frame: np.ndarray, verbose: bool = False): Save a photo from the camera.
        _increment_photo_counter(value: int = 1): Update the photo counter
        calibrate(): Calibrate the sensor
        initialize(): Initializes the camera
        read(): Captures an image from the camera
        stream_video(): Displays the live video feed from the camera
        record_video(): Record a video from the camera
        release(): Releases the camera resources when done
    """

    def __init__(self, name: str = "RPi Camera",
                 photo_path: Path = Path("data/images/samples"), photo_name: str = 'rpi_photo',
                 video_path: Path = Path("data/videos/samples"), video_name: str = 'rpi_video'):
        """
        Initializes the camera object to None.

        Args:
            name (str): The name of the camera.
            photo_path (Path): The path to save photos.
            photo_name (str): The name of the photo.
            video_path (Path): The path to save videos.
            video_name (str): The name of the video.
        """
        super().__init__(name, s_type=SensorType.RPI_CAMERA, 
                         photo_path=photo_path, photo_name=photo_name,
                         video_path=video_path, video_name=video_name)

    # ----- protected methods

    # ----- public methods

    def initialize(self) -> None:
        """
        Initializes the rpi's webcam using OpenCV.

        Raises:
            RPiCameraException: If there is an error opening the rpi's cam.
        """
        self._camera = Picamera2()
        mode = self._camera.sensor_modes[0]
        # camera_config = self._camera.create_preview_configuration(main={"format": "RGB888"},
        #                                                           sensor={"output_size": mode['size'],
        #                                                                 "bit_depth": mode['bit_depth']})
        # camera_config = self._camera.create_preview_configuration(main={"size": (640, 480)})
        camera_config = self._camera.create_video_configuration(main={"format": "RGB888", "size": self._resolution, "preserve_ar": False},
                                                                controls = {"NoiseReductionMode": 0, "FrameDurationLimits": (33333, 33333)})
        print(camera_config)
        self._camera.configure(camera_config)

        # Controls
        self._camera.set_controls({
            "AfMode": 0,        # Enfoque manual
            "LensPosition": 1,
            "AeEnable": False,
            "ExposureTime": 3500,
            # "AnalogueGain": 1.0,
            # "AwbEnable": False,
            # "ColourGains": (1.5, 1.5)
            # "Contrast": 1.2
        })

        # self._camera.set_controls({"ExposureMode": "off"})
        # self._camera.set_controls({"AwbMode": "off"})

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
        return frame

    # Deprecated (with opencv is more efficient and compatible with other cameras)
    def record_video_d(self, ending: str = 'mp4', duration: int = 5, verbose: bool = False) -> None:
        """
        record a video from the rpi's camera.

        Args:
            filename (str): The filename to save the video.
            ending (str): The file ending of the video.
            duration (int): The duration of the video in seconds.
            verbose (bool): If True, print the filename of the video saved.
        """
        self._increment_counter('video')
        filepath = self._video_path / f"{self._video_name}_{self._video_counter}.{ending}"

        self._camera = Picamera2()
        self._camera.configure(self._camera.create_video_configuration())
        encoder = H264Encoder()
        if verbose:
            print(f"Recording video for {duration} seconds...")
        self._camera.start_recording(encoder, str(filepath), quality=Quality.HIGH)
        time.sleep(10)
        self._camera.stop_recording()

        if verbose:
            print(f"Video saved as {filepath}")

    def release(self):
        """
        Releases the camera resources when done.
        """
        if self._camera:
            self._camera.close()
            self._camera = None
            print(f"RPi Camera ({self._name}) released.")
