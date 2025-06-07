"""
main.py
"""

from src.coordinator import Coordinator


def main():
    """
    main function
    """
    coordinator = Coordinator('rpi_camera')
    coordinator.run()



if __name__ == '__main__':
    main()
