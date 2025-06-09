"""
sensor_detector_simulation.py
"""

import cv2
import numpy as np

from src.sensor.sensor_type import SensorType
from src.factory import SensorFactory

from src.sensor.rpi_camera import RPiCamera
from src.detector.color_detector import ColorDetector
from src.classifier import LabClassifier
from src.utils import bgr_to_lab


def loop(detector: ColorDetector, image: np.ndarray):
    """
    Main Loop
    """
    threshold_image, pieces = detector.detect(image, merge_pieces=False)

    for piece in pieces:
        piece_mean_color_bgr = piece.calculate_mean_color()
        piece_mean_color_lab = bgr_to_lab(piece_mean_color_bgr)
        material, dist = LabClassifier.which_material(piece_mean_color_lab)
        piece.name = f"{material}{dist}"    # piece.id
        piece.draw(image)

    return image, threshold_image


def main():
    """
    Main
    """
    camera: RPiCamera = SensorFactory.create(SensorType.RPI_CAMERA)
    detector = ColorDetector(thresh=80, min_area=1000)

    camera.initialize()
    detector.initialize()

    # main loop
    while True:
        image = camera.read()
        image, threshold_image = loop(detector, image)
        cv2.imshow('Video', cv2.vconcat([threshold_image, image]))
        cv2.moveWindow('Video', 1200, 50)
        # Quit pressing 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
