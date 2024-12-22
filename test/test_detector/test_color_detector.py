"""
test_color_detector.py
"""

import cv2

from src.detector.base_detector import DetectorException
from src.detector.color_detector import ColorDetector

from src.utils import show_image


def test_initialize_detector(cdetector: ColorDetector) -> None:
    """
    test
    """
    try:
        result = cdetector.initialize()
        if result:
            print('YES')
    except DetectorException:
        print('NO')


def test_detect(cdetector: ColorDetector) -> None:
    """
    test
    """
    filename = r'data\images\samples\cobre_1.jpeg'
    filename = r'data\images\samples\laton_1.jpeg'
    # filename = r'data\images\samples\zinc_1.jpeg'
    image = cv2.imread(filename)
    image = cv2.resize(image, (640, 640))
    show_image(image)
    r_image = cdetector.detect(image)
    show_image(r_image)


def main():
    """
    main
    """
    cdetector = ColorDetector((255, 255, 255), (0, 0, 0))
    test_initialize_detector(cdetector)
    test_detect(cdetector)


if __name__ == '__main__':
    main()
