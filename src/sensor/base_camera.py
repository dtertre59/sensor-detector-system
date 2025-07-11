"""
camera.py
"""

import time
from pathlib import Path
import numpy as np
import cv2

from src.sensor.base_sensor import BaseSensor, SensorException
from src.sensor.sensor_type import SensorType

from src.utils import obtain_filenames_last_number


class CameraException(SensorException):
    """
    Camera Exception
    """


class BaseCamera(BaseSensor):
    """
    Base interface for all camera types.
    Defines the common methods that all camera implementations must provide.

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

    def __init__(self, name: str = "Camera", camera_id: int = 0, s_type: SensorType = SensorType.CAMERA,
                 photo_path: Path = Path("data/images/samples"), photo_name: str = 'photo',
                 video_path: Path = Path("data/videos/samples"), video_name: str = 'video'):
        """
        Initializes the camera object to None.

        Args:
            name (str): The name of the camera.
            camera_id (int): The camera ID.
            s_type (SensorType): The type of the camera.
            photo_path (Path): The path to save photos.
            photo_name (str): The name of the photo.
        """
        self._name = name
        self._camera_id = camera_id
        self._type = s_type
        self._status = "idle"

        self._photo_path = photo_path
        self._photo_name = photo_name
        try:
            self._photo_counter = obtain_filenames_last_number(self._photo_path, self._photo_name, verbose=False)
        except:
            self._photo_counter = 0

        self._video_path = video_path
        self._video_name = video_name
        try:
            self._video_counter = obtain_filenames_last_number(self._video_path, self._video_name, verbose=False)
        except:
            self._video_counter = 0

        self._camera = None
        self._resolution = (640, 480)  # (1536, 864)
        self._camera_config = None

        self.__output_video = None
        self.__video_recorder_flag = 0
        self.__framerate = 0

    # ----- Properties and Setters

    @property
    def name(self) -> str:
        """
        Get the name of the camera

        Returns:
            str: The name of the camera
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the camera

        Args:
            value (str): The name of the camera
        """
        if not isinstance(value, str):
            raise CameraException("The name of the camera must be a string.")
        self._name = value

    @property
    def camera_id(self) -> int:
        """
        Get the camera ID

        Returns:
            int: The camera ID
        """
        return self._camera_id

    @camera_id.setter
    def camera_id(self, value: int) -> None:
        """
        Set the camera ID

        Args:
            value (int): The camera ID
        """
        if not isinstance(value, int):
            raise CameraException("The camera ID must be an integer.")
        self._camera_id = value

    @property
    def type(self) -> SensorType:
        """
        Get the type of the camera

        Returns:
            SensorType: The type of the camera
        """
        return self._type

    @type.setter
    def type(self, value: SensorType) -> None:
        """
        Set the type of the camera

        Args:
            value (SensorType): The type of the camera
        """
        if not isinstance(value, SensorType):
            raise CameraException("The type of the camera must be a SensorType object.")
        self._type = value

    @property
    def status(self) -> str:
        """
        Get the status of the camera

        Returns:
            str: The status of the camera
        """
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        """
        Set the status of the camera

        Args:
            value (str): The status of the camera
        """
        if not isinstance(value, str):
            raise CameraException("The status of the camera must be a string.")
        self._status = value

    @property
    def photo_path(self) -> Path:
        """
        Get the path to save photos

        Returns:
            Path: The path to save photos
        """
        return self._photo_path

    @photo_path.setter
    def photo_path(self, value: Path) -> None:
        """
        Set the path to save photos

        Args:
            value (Path): The path to save photos
        """
        if not isinstance(value, Path):
            raise CameraException("The path to save photos must be a Path object.")
        self._photo_path = value

    @property
    def photo_name(self) -> str:
        """
        Get the name of the photo

        Returns:
            str: The name of the photo
        """
        return self._photo_name

    @photo_name.setter
    def photo_name(self, value: str) -> None:
        """
        Set the name of the photo

        Args:
            value (str): The name of the photo
        """
        if not isinstance(value, str):
            raise CameraException("The name of the photo must be a string.")
        self._photo_counter = obtain_filenames_last_number(self._photo_path, value)
        self._photo_name = value

    @property
    def photo_counter(self) -> int:
        """
        Get the photo counter

        Returns:
            int: The photo counter
        """
        return self._photo_counter

    @photo_counter.setter
    def photo_counter(self, value: int) -> None:
        """
        Set the photo counter

        Args:
            value (int): The photo counter
        """
        if not isinstance(value, int):
            raise CameraException("The photo counter must be an integer.")
        self._photo_counter = value

    @property
    def video_path(self) -> Path:
        """
        Get the path to save videos

        Returns:
            Path: The path to save videos
        """
        return self._video_path

    @video_path.setter
    def video_path(self, value: Path) -> None:
        """
        Set the path to save videos

        Args:
            value (Path): The path to save videos
        """
        if not isinstance(value, Path):
            raise CameraException("The path to save videos must be a Path object.")
        self._video_path = value

    @property
    def video_name(self) -> str:
        """
        Get the name of the video

        Returns:
            str: The name of the video
        """
        return self._video_name

    @video_name.setter
    def video_name(self, value: str) -> None:
        """
        Set the name of the video

        Args:
            value (str): The name of the video
        """
        if not isinstance(value, str):
            raise CameraException("The name of the video must be a string.")
        self._video_counter = obtain_filenames_last_number(self._video_path, value)
        self._video_name = value

    @property
    def video_counter(self) -> int:
        """
        Get the video counter

        Returns:
            int: The video counter
        """
        return self._video_counter

    @video_counter.setter
    def video_counter(self, value: int) -> None:
        """
        Set the video counter

        Args:
            value (int): The video counter
        """
        if not isinstance(value, int):
            raise CameraException("The video counter must be an integer.")
        self._video_counter = value

    # ----- protected methods

    def _is_init(self) -> bool:
        """
        Is camera init.

        Returns:
            bool
        """
        if self._camera:
            return True
        print("Camera not initialized.")
        return False

    def _increment_counter(self, option: str = 'photo', value: int = 1) -> None:
        """
        Update the photo counter

        Args:
            option (str): 'photo' or 'video'
            n (int): counter increment
        """
        if option == 'photo':
            self._photo_counter += value
        elif option == 'video':
            self._video_counter += value
        else:
            raise ValueError('Option must be "photo" or "video".')

    def _save_photo(self, frame: np.ndarray, verbose: bool = False) -> None:
        """
        Save a photo from the camera.

        Args:
            frame (np.ndarray): The image frame from the camera.
            verbose (bool): Print the photo filename.
        """
        self._increment_counter('photo')
        photo_filename = self._photo_path / f"{self._photo_name}_{self._photo_counter}.png"
        cv2.imwrite(str(photo_filename), frame)
        if verbose:
            print(f"Photo saved as {photo_filename}")

    def _record_video(self, frame: np.ndarray, verbose: bool = False) -> None:
        """
        record video TODO
        """
        if self.__video_recorder_flag == 0:
            return
        elif self.__video_recorder_flag == 2:
            if verbose:
                print('Setup video recorder')
            # setup video record
            self._increment_counter('video')
            filepath = self._video_path / f"{self._video_name}_{self._video_counter}.mp4"
            codec = cv2.VideoWriter_fourcc(*'mp4v')
            # Create a VideoWriter object for writing the output video
            fps = 29
            self.__output_video = cv2.VideoWriter(str(filepath), codec, fps, self._resolution)
            self.__video_recorder_flag = 1
            if verbose:
                print('Video recording ...')
        elif self.__video_recorder_flag == 1:
            self.__output_video.write(frame)
            cv2.putText(frame, 'Recording video ...', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        elif self.__video_recorder_flag == -1:
            self.__output_video.release()
            self.__video_recorder_flag = 0
            if verbose:
                filepath = self._video_path / f"{self._video_name}_{self._video_counter}.mp4"
                print(f'video recorded as {filepath}')
        else:
            raise ValueError(f'Video recorder flag. invalid value {self.__video_recorder_flag}')

    # ----- public methods

    # ----- Not implemented in the base class

    def calibrate(self) -> None:
        """
        Calibrate the camera
        """

    def initialize(self) -> None:
        """
        Initializes the camera.
        """

    # REVIEW 
    def read(self) -> np.ndarray:
        """
        Captures an image from the camera.

        Returns:
            np.ndarray: The image captured from the camera.

        Raises:
            CameraException: If there is an error grabbing the frame.
        """
        frame = self._camera.read()
        if not frame:
            raise CameraException("Failed to grab frame.")
        return frame

    def stream_video(self, show_fps: bool = False, verbose: bool = False) -> None:
        """
        Displays the live video feed from the rpi's cam.

        Options:
            - Press 'q' to quit
            - Press 's' | 'S' | ' ' to save a photo
            - Press 'r' | 'R' to start and stop recording

        Args:
            verbose (bool): If True, print the filename of the photo saved.
        """
        if not self._is_init():
            return
        
        self.__video_recorder_flag = 0

        # Initialize variables for FPS calculation
        fps = 0
        prev_time = time.time()

        if verbose:
            print("Press 'q' key to stop the live video feed.")
        while True:
            frame = self.read()

            # start/stop video recording
            if self.__video_recorder_flag != 0:
                self._record_video(frame, verbose)

            # Calculate FPS
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            self.__framerate=fps # se puede quitar esta variables TODO
            prev_time = current_time
            
            if show_fps:
                cv2.putText(frame, f"FPS: {fps:.2f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)


            cv2.imshow(f'{self._name} live streaming', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # ASCII code for 'q'
                # quit
                break
            if key == 32 or key == ord('s') or key == ord('S'):  # Space key or 's' key
                # save photo
                self._save_photo(frame, verbose)
            if key == ord('r') or key == ord('R'):
                if self.__video_recorder_flag == 0:
                    # Start recording
                    self.__video_recorder_flag = 2
                elif self.__video_recorder_flag == 1:
                    # Stop recording
                    self.__video_recorder_flag = -1



        cv2.destroyAllWindows()

    def record_video(self) -> None:
        """
        Record a video from the camera.
        """

    def record_video_standar(self, ending: str = 'mp4', duration: int = 5, verbose: bool = False) -> None:
        """
        Record a video from the camera.

        Args:
            ending (str): The video file extension.
            duration (int): The duration of the video recording in seconds.
            verbose (bool): If True, print the filename of the photo saved.

        Raises:
            CameraException: If there is an error grabbing the frame.
        """
        if not self._is_init():
            return

        self._increment_counter('video')
        filepath = self._video_path / f"{self._video_name}_{self._video_counter}.{ending}"
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        framerate = 30
        resolution = (640, 480)

        # Create a VideoWriter object for writing the output video
        out = cv2.VideoWriter(str(filepath), codec, framerate, resolution)


        while True:
            frame = self.read()

            if frame is None:
                continue

            frame = cv2.resize(frame, resolution)
            out.write(frame)

            cv2.imshow('Frame', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # ASCII code for 'q'
                # quit
                break
            if key == 32 or key == ord('s') or key == ord('S'):  # Space key or 's' key
                # save photo
                self._save_photo(frame, verbose)
        out.release()
        cv2.destroyAllWindows()



    def release(self) -> None:
        """
        Releases the camera resources when done.
        """
