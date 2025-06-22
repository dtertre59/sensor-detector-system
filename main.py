"""
main.py
"""

import src.config_vars as cfv
from src.coordinator import Coordinator


def main():
    """
    main function
    """
    coordinator = Coordinator(
        sensor_name='rpi_camera',
        detector_name='color_detector',
        host=cfv.HOST,
        port=cfv.PORT)
    coordinator.run()



if __name__ == '__main__':
    main()
