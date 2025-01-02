"""
test_detector_factory.py
"""

from src.factory import DetectorFactory
from src.detector.detector_type import DetectorType


def test_color_detector_instance():
    """
    test
    """
    detector = DetectorFactory().create(DetectorType.COLOR_DETECTOR)
    if detector.get_type() == DetectorType.COLOR_DETECTOR:
        print('OK')
    else:
        print('NO')


def main():
    """
    main
    """
    test_color_detector_instance()


if __name__ == '__main__':
    main()
