"""
sensor_detector_simulation.py
"""

import struct

import cv2

from src.detector.color_detector import ColorDetector
from src.tracker import Tracker
from src.coordinator import Classifier

from src.transmitter import MulticastTransmitter


def main_image_sequence():
    """
    main
    """
    detector = ColorDetector(min_area=1000)
    tracker = Tracker()

    background = cv2.imread('data/images/background/background_0.png')
    
    detector.flat_field = background

    # Bucle de imagenes
    for i in range(10):
        frame = cv2.imread(f'data/images/sequence/sample_{i}.png')

        pieces = detector.detect(frame, verbose=False)  # OK
        tracker.update_3(pieces, verbose=True)  # TODO va mal al hechar las piezas
        tracker.draw(frame, track=False)

        # Mostrar el cuadro
        cv2.imshow('Video', frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        input('Press enter to continue...')

    cv2.destroyAllWindows()


class RawPiece():
    """
    Class Raw Piece
    """
    def __init__(self, material: int, timestamp: int):
        self.material = material
        self.timestamp = timestamp

    def pack(self) -> bytes:
        """
        Pack the RawPiece data into bytes for transmission.
        Resturns:
            bytes:∫ representation of the RawPiece
        """
        return struct.pack('II', self.material, self.timestamp)


def main_video():
    """
    main
    """
    detector = ColorDetector()
    tracker = Tracker()
    transmitter = MulticastTransmitter('224.0.0.1', 5007)
    transmitter.initialize()

    # Ruta del archivo .avi
    archivo_mp4 = 'data/videos/samples/full_video_tspeed2_1.mp4'
    cap = cv2.VideoCapture(archivo_mp4)
    # Verificar si se abrió correctamente
    if not cap.isOpened():
        print("Error opening video file.")
        exit()

    flag = False

    # Bucle de imagenes
    while True:
        # Leer un cuadro del video
        ret, frame = cap.read()

        # Si no se puede leer un cuadro, terminamos
        if not ret:
            print("End of video.")
            break

        if flag:
            detector.flat_field = frame
            flag = False

        pieces = detector.detect(frame, verbose=False)
        released_pieces = tracker.update_3(pieces, verbose=False)

        for piece in tracker._pieces:
            material = Classifier.which_material(piece.calculate_mean_color())
            piece.name = f"{material}-{piece.id}"

        if released_pieces:
            print('Released pieces:', [released_piece.name for released_piece in released_pieces])
            for piece in released_pieces:
                material = Classifier.which_material(piece.calculate_mean_color())
                material_id = 0
                if material == 'zinc':
                    material_id = 1

                data_raw = RawPiece(material_id, int(piece.positions[-1]['time'])).pack()
                transmitter.send_multicast(data_raw)
                print('Sent:', piece.name)

        tracker.draw(frame)

        # Mostrar el cuadro
        cv2.imshow('Video', frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Liberar el objeto de captura y cerrar todas las ventanas
        # input('Frame size: ' + str(frame.shape) + '\nPress enter to continue...')

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # main_image_sequence()
    main_video()
