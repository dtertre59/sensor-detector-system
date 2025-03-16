"""
sensor_detector_simulation.py
"""

import cv2

from src.detector.color_detector import ColorDetector
from src.tracker import Tracker

from src.transmitter import Transmitter


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


def main_video():
    """
    main
    """
    detector = ColorDetector()
    tracker = Tracker()
    transmitter = Transmitter("localhost", 5001)

    transmitter.initialize()

    # Ruta del archivo .avi
    archivo_mp4 = 'data/videos/samples/full_video_2.mp4'
    cap = cv2.VideoCapture(archivo_mp4)
    # Verificar si se abrió correctamente
    if not cap.isOpened():
        print("Error opening video file.")
        exit()

    flag = True

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
        if released_pieces:
            print('Released pieces:', [released_piece.name for released_piece in released_pieces])
            for piece in released_pieces:
                transmitter.send_piece(piece.name)
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
