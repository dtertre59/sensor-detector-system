"""
color_detector.py
"""

import numpy as np
import cv2

from src.detector.base_detector import BaseDetector, DetectorException
from src.detector.detector_type import DetectorType

from src.detector import utils as dut
from src.piece.piece import Piece
# import src.utils as ut


class ColorDetectorException(DetectorException):
    """
    Exception class for color detector errors.
    """


class ColorDetector(BaseDetector):
    """
    A color detector class implementing the DetectorInterface to detect specific colors in an image.
    """

    def __init__(self, name: str = 'detector-image-color', thresh: int = 150, min_area: int = 135):
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
        self._thresh = thresh
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
        noise_free_flat_field = dut.reduce_noise(flat_field, (31, 31))
        gray_flat_field = cv2.cvtColor(noise_free_flat_field, cv2.COLOR_BGR2GRAY)
        self._flat_field = gray_flat_field

    def reset(self):
        """
        Resets the detector, clearing any internal states or buffers.
        """
        self._name = 'detector-image-color'
        self.detection_result = None
        # self._thresh = 150
        # self._min_area = 135
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

    def detect(self, image: np.ndarray,
               merge_pieces: bool = True, verbose: bool = False) -> tuple[np.ndarray, list[Piece]]:
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
        noise_free_image = dut.reduce_noise(image, (31, 31))

        # Convert to gray
        gray_image = cv2.cvtColor(noise_free_image, cv2.COLOR_BGR2GRAY)
        # ut.show_image(gray_image)

        # # Segment image
        # threshold_image = dut.segment(gray_image, self._min_area, verbose)

        # Segment image 2
        threshold_image = dut.segment(gray_image, thresh=self._thresh,
                                      min_area=self._min_area, flat_field=self._flat_field,
                                      verbose=verbose)
        # ut.show_image(threshold_image)

        # Find connected components
        # num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(threshold_image)
        # threshold_image = dut.delete_small_labels(threshold_image, self._min_area, verbose)
        # ut.show_image(threshold_image)

        # Morphological operations to unite close components
        # kernel = np.ones((25, 25), np.uint8)  # You can adjust the kernel size as needed
        # kernel = np.ones((1, 1), np.uint8)  # You can adjust the kernel size as needed

        # dilated_image = cv2.dilate(threshold_image, kernel, iterations=1)
        # eroded_image = cv2.erode(dilated_image, kernel, iterations=1)
        eroded_image = threshold_image.copy()
        # threshold_image = eroded_image.copy()

        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(eroded_image)
        # ut.show_image(threshold_image)
        # cv2.waitKey(1)

        # join close components
        if merge_pieces:    # Recorremos cada par de componentes (ignoramos el fondo: label 0)
            grow_rectangle = 3  # Tolerance for merging components
            for i in range(1, num_labels):
                x1, y1, w1, h1, _ = stats[i]
                rect1 = (x1 - grow_rectangle, 
                         y1 - grow_rectangle, 
                         x1 + w1 + grow_rectangle*2, 
                         y1 + h1 + grow_rectangle*2)  # (x1_min, y1_min, x1_max, y1_max)

                for j in range(i + 1, num_labels):
                    x2, y2, w2, h2, _ = stats[j]
                    rect2 = (x2 - grow_rectangle, 
                             y2 - grow_rectangle, 
                             x2 + w2 + grow_rectangle*2, 
                             y2 + h2 + grow_rectangle*2)  # (x1_min, y1_min, x1_max, y1_max)

                    # Verificar si las bounding boxes se tocan o se solapan
                    intersectan = not (
                        rect1[2] < rect2[0] or rect2[2] < rect1[0] or
                        rect1[3] < rect2[1] or rect2[3] < rect1[1]
                    )

                    if intersectan:
                        # Obtener los centros
                        centro1 = tuple(map(int, centroids[i]))
                        centro2 = tuple(map(int, centroids[j]))

                        # Dibujar línea blanca que los una
                        cv2.line(eroded_image, centro1, centro2, 255, thickness=2)
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(eroded_image)

        # Create Pieces
        pieces: list[Piece] = []

        for label in range(1, num_labels):
            x, y, w, h, area = stats[label]

            # Why? TODO - Check
            # mean_color = dut.get_mean_color_from_image(threshold_image, image)
            # position = dut.get_gravity_center(threshold_image)
            mean_color = None
            position = None

            piece = Piece(id=0, name='piece', bbox=(int(x), int(y), int(w), int(h)),
                          mean_color=mean_color, position=position, area=int(area))

            # # Change to LAB format
            # image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
            # image = image_lab
            piece.add_mean_color(dut.get_mean_color_from_label(label, labels, image))
            piece.add_position(tuple(map(int, centroids[label])))

            pieces.append(piece)

        # Draw images
        if 0: 
            gray_image_bgr = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
            threshold_image_bgr = cv2.cvtColor(threshold_image, cv2.COLOR_GRAY2BGR)
            eroded_image_bgr = cv2.cvtColor(eroded_image, cv2.COLOR_GRAY2BGR)
            for piece in pieces:
                piece.draw(eroded_image_bgr)
            row1 = cv2.hconcat([image, gray_image_bgr])
            row2 = cv2.hconcat([threshold_image_bgr, eroded_image_bgr])
            matrix = cv2.vconcat([row1, row2])
            cv2.imshow('Video Threshold process', matrix)

        return eroded_image, pieces

    def release(self):
        """
        Relase
        """
        self._status = "idle"
        print('Detector release')
