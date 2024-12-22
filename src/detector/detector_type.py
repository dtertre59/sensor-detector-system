"""
DetectorType is an enumeration of the different types of detectors that can be.
"""

from enum import Enum


class DetectorType(Enum):
    """
    SensorType is an enumeration of the different types of sensors that can be
    used in the system. This is used to specify the type of sensor that is
    being used in the system.
    """
    COLOR_DETECTOR = "color_detector"
