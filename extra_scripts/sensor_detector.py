"""
sensor_detector_simulation.py
"""

import struct

import cv2

from src.sensor.sensor_type import SensorType
from src.factory import SensorFactory

from src.sensor.rpi_camera import RPiCamera
from src.detector.color_detector import ColorDetector
from src.tracker import Tracker
from src.coordinator import Classifier

from src.transmitter import MulticastTransmitter


def main():
    """
    main
    """
    camera: RPiCamera = SensorFactory.create(SensorType.RPI_CAMERA)
    detector = ColorDetector(thresh=80, min_area=1000)

    camera.initialize()
    detector.initialize()

    # Bucle de imagenes
    while True:
        frame = camera.read()

        threshold_image, pieces = detector.detect(frame, merge_pieces=False)

        for piece in pieces:
            material = Classifier.which_material(piece.calculate_mean_color())
            piece.name = f"{material}" #  piece.id
            piece.draw(frame)

        # Mostrar el cuadro
        cv2.imshow('Video', cv2.vconcat([threshold_image, frame]))
        cv2.moveWindow('Video', 1200, 50)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # input('Press enter to continue...')

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
