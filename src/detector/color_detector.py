"""
color_detector.py
"""

import cv2

from src.detector.base_detector import BaseDetector, DetectorException


class ColorDetectorException(DetectorException):
    """
    Exception class for color detector errors.
    """


class ColorDetector(BaseDetector):
    """
    A color detector class implementing the DetectorInterface to detect specific colors in an image.
    """

    def __init__(self, target_color_lower: int = 50, target_color_upper: int = 245):
        """
        Initializes the color detector.

        Args:
            target_color_lower (tuple): The lower bound of the color in HSV format (e.g., (0, 100, 100)).
            target_color_upper (tuple): The upper bound of the color in HSV format (e.g., (10, 255, 255)).
        """
        self.target_color_lower = target_color_lower
        self.target_color_upper = target_color_upper
        self.status = "idle"
        self.detection_result = None

    def process_detection(self, detection_result):
        """
        Processes the result of a detection.

        Args:
            detection_result (dict): A dictionary containing the detection result.
        """

    def reset(self):
        """
        Resets the detector, clearing any internal states or buffers.
        """

    def get_status(self):
        """
        Returns the current status of the detector (e.g., whether it's active or idle).

        Returns:
            str: The status of the detector.
        """

    def initialize(self):
        """
        Initializes the color detector.
        """
        print("Color detector initialized.")
        self.status = "active"

    def detect(self, image):
        """
        Detects a specific color in the provided image.

        Args:
            image (numpy.ndarray): The image from the camera.

        Returns:
            bool: True if the target color is detected, False otherwise.
        """
        # Convertir la imagen a escala de grises (no es necesario si ya tienes la imagen a color)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Crear un objeto CLAHE con un límite de contraste
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))

        # Aplicar CLAHE a la imagen en escala de grises
        enhanced_image = clahe.apply(gray_image)

        # Convertir de nuevo a BGR para la imagen original a color
        enhanced_image = cv2.cvtColor(enhanced_image, cv2.COLOR_GRAY2BGR)

        return enhanced_image
        # Convert the image to HSV color space
        # hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # # Definir el rango de saturación para los píxeles no grises
        # # Los grises tendrán una saturación baja, así que filtramos los píxeles con saturación baja
        # lower_saturation = 90  # Valor bajo de saturación, ajustable según la imagen
        # upper_saturation = 255  # Valor alto de saturación

        # # Filtrar los píxeles con baja saturación (grises)
        # lower_bound = np.array([0, lower_saturation, 0])  # Rango de HSV para excluir el gris
        # upper_bound = np.array([180, upper_saturation, 255])

        # # Crear la máscara
        # mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        # # Aplicar la máscara a la imagen original
        # filtered_image = cv2.bitwise_and(image, image, mask=mask)

        # return filtered_image

        # # Create a mask based on the target color range
        # mask = cv2.inRange(hsv_image, self.target_color_lower, self.target_color_upper)

        # # Find contours of the detected color
        # contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # # If any contours are found, it means the color is detected
        # if contours:
        #     self.detection_result = {"color": True, "location": contours}
        #     print("Target color detected!")
        #     return True
        # else:
        #     self.detection_result = {"color": False, "location": None}
        #     print("Target color not detected.")
        #     return False
