"""
color_detector.py
"""

import numpy as np
import cv2

from src.detector.base_detector import BaseDetector, DetectorException
from src.detector.detector_type import DetectorType

from src.detector import utils
from src.piece.piece import Piece
import src.utils as ut


class ColorDetectorException(DetectorException):
    """
    Exception class for color detector errors.
    """


class ColorDetector(BaseDetector):
    """
    A color detector class implementing the DetectorInterface to detect specific colors in an image.
    """

    def __init__(self, name: str = 'detector-image-color', min_area: int = 135):
        """
        Initializes the color detector.

        Args:
            target_color_lower (tuple): The lower bound of the color in HSV format (e.g., (0, 100, 100)).
            target_color_upper (tuple): The upper bound of the color in HSV format (e.g., (10, 255, 255)).
        """
        self._name = name
        self._status = "idle"
        self._type = DetectorType.COLOR_DETECTOR

        self.detection_result = None

        self._min_area = min_area
        self._flat_field = None

    @property
    def flat_field(self):
        """
        Get flat field
        """
        return self._flat_field
    
    @flat_field.setter
    def flat_field(self, flat_field: np.ndarray):
        """
        Set flat field
        """
        noise_free_flat_field = utils.reduce_noise(flat_field, (31, 31))
        gray_flat_field = cv2.cvtColor(noise_free_flat_field, cv2.COLOR_BGR2GRAY)
        self._flat_field = gray_flat_field

    def reset(self):
        """
        Resets the detector, clearing any internal states or buffers.
        """
        self._name = 'detector-image-color'
        self.detection_result = None
        self._min_area = 135
        self._status = "idle"

    def get_status(self):
        """
        Returns the current status of the detector (e.g., whether it's active or idle).

        Returns:
            str: The status of the detector.
        """
        return self._status

    def get_type(self) -> DetectorType:
        """
        Returns the type of the detector.

        Returns:
            DetectorType: The type of the detector.
        """
        return self._type

    def initialize(self):
        """
        Initializes the color detector.
        """
        print("Color detector initialized.")
        self._status = "active"

    def detect(self, image: np.ndarray, verbose: bool = False) -> list[Piece]:
        """
        Detects a specific color in the provided image.

        Args:
            image (np.ndarray): an image.

        Returns:
            list[Pieces]: A list of pieces.
        """
        # Resize image
        # image = cv2.resize(image, (640, 640))

        # Reduce noise
        noise_free_image = utils.reduce_noise(image, (31, 31))

        # Convert to gray
        gray_image = cv2.cvtColor(noise_free_image, cv2.COLOR_BGR2GRAY)
        # ut.show_image(gray_image)

        # # Segment image
        # threshold_image = utils.segment(gray_image, self._min_area, verbose)

        # Segment image 2
        threshold_image = utils.segment_2(gray_image, self._min_area, flat_field=self._flat_field, verbose=verbose)

        # ut.show_image(threshold_image)

        # Find connected components
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(threshold_image)
        # ut.show_image(threshold_image)

        # Morphological operations to unite close components
        kernel = np.ones((25, 25), np.uint8)  # You can adjust the kernel size as needed
        dilated_image = cv2.dilate(threshold_image, kernel, iterations=1)
        eroded_image = cv2.erode(dilated_image, kernel, iterations=1)
        threshold_image = eroded_image.copy()

        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(threshold_image)
        # ut.show_image(threshold_image)

        # cv2.imshow('Video threshold', threshold_image)
        # cv2.waitKey(1)

        # Create Pieces
        pieces: list[Piece] = []

        for label in range(1, num_labels):
            x, y, w, h, area = stats[label]

            # Why? TODO - Check
            # mean_color = utils.get_mean_color_from_image(threshold_image, image)
            # position = utils.get_gravity_center(threshold_image)
            mean_color = None
            position = None

            piece = Piece(id=0, name='piece', bbox=(int(x), int(y), int(w), int(h)), mean_color=mean_color,
                          position=position, area=int(area))
            piece.add_mean_color(utils.get_mean_color_from_label(label, labels, image))
            piece.add_position(tuple(map(int, centroids[label])))

            pieces.append(piece)

        return pieces

    def release(self):
        """
        Relase
        """
        self._status = "idle"
        print('Detector release')
