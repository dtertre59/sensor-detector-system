"""
computer_camera.py
"""

# import time
# import cv2

from src.sensor.base_camera import BaseCamera, CameraException


class ComputerCameraException(CameraException):
    """
    Computer Camera Exception
    """


class ComputerCamera(BaseCamera):
    """
    Camera implementation for the computer's webcam using OpenCV.
    """

    def __init__(self):
        """
        Initializes the camera object to None.
        """
        self.camera = None

    def read_value(self):
        """
        Read a value from the sensor
        """

    def calibrate(self):
        """
        Calibrate the sensor
        """

    def get_status(self):
        """
        Get the status of the sensor
        """

    def initialize(self):
        """
        Initializes the camera.
        """
        self.camera = 1

    def capture_image(self):
        """
        Captures an image from the camera.

        Returns:
            str: The filename of the captured image.
        """
        filename = "computer_webcam.jpg"
        return filename

    def release(self):
        """
        Releases the camera resources when done.
        """
        self.camera = None

    def show_live_video(self):
        """
        Displays the live video feed from the computer's webcam until
        a key is pressed.
        """

    # def _is_init(self) -> bool:
    #     """
    #     Is camera init

    #     Returns:
    #         bool
    #     """
    #     if self.camera:
    #         return True
    #     print("Camera not initialized.")
    #     return False

    # def initialize(self) -> bool:
    #     """
    #     Initializes the computer's webcam using OpenCV.

    #     Raises an exception if the camera cannot be opened.
    #     """
    #     self.camera = cv2.VideoCapture(0)  # 0 is the default webcam index
    #     if not self.camera.isOpened():
    #         raise CameraException("Error opening computer webcam.")
    #     else:
    #         print("Computer webcam initialized.")
    #     return True

    # def capture_image(self):
    #     """
    #     Captures an image from the computer's webcam.

    #     Returns:
    #         str: The filename of the captured image.
    #     """
    #     if not self._is_init():
    #         return None

    #     ret, frame = self.camera.read()
    #     if ret:
    #         filename = f"computer_webcam_{time.time()}.jpg"
    #         cv2.imwrite(filename, frame)
    #         cv2.imshow('ccamera', frame)
    #         print(f"Image captured: {filename}")
    #         # Wait for a key press and close the window
    #         cv2.waitKey(0)  # Wait indefinitely until a key is pressed
    #         cv2.destroyAllWindows()  # Close the OpenCV window after key press
    #         return frame, filename
    #     else:
    #         print("Failed to capture image.")
    #         return None

    # def release(self):
    #     """
    #     Releases the computer webcam resources.

    #     Closes the camera connection and frees the resources.
    #     """
    #     if self._is_init():
    #         self.camera.release()
    #         print("Computer webcam released.")

    # def show_live_video(self):
    #     """
    #     Displays the live video feed from the computer's webcam until a key is pressed.
    #     """
    #     if not self._is_init():
    #         return

    #     print("Press any key to stop the live video feed.")
    #     while True:
    #         ret, frame = self.camera.read()
    #         if not ret:
    #             print("Failed to capture frame.")
    #             break

    #         # Display the live video feed
    #         cv2.imshow('Computer CAM live video feed', frame)

    #         # Wait for a key press and exit the loop if a key is pressed
    #         if cv2.waitKey(1) & 0xFF != 255:
    #             break

    #     # Close the video feed window after exiting the loop
    #     cv2.destroyAllWindows()
