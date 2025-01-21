"""
test_video_follow.py
"""
import time
import cv2

from src.utils import show_image
from src.detector.color_detector import ColorDetector
from src.tracker import Tracker
from src.piece.piece import Piece


def test_image_follow() -> None:
    """
    test
    """
    detector = ColorDetector()
    tracker = Tracker()
    images_path = 'data/images/samples/'
    images_name = 'photo'
    n = 4
    for i in range(1, n+1):
        print('Photo', i)
        filename = images_path + images_name + '_' + str(i) + '.png'
        frame = cv2.imread(filename)
        pieces = detector.detect(frame, verbose=True)
        pieces = tracker.update(pieces)
        tracker.draw(frame)
        print('len', len(pieces))
        if len(pieces) > 0:
            break
    for piece in pieces:
        sp = piece.calculate_speed()
        print('Speed: ', sp)
        mc = piece.calculate_mean_color()
        print('Mean color', mc)

        print('last position', piece.get_last_positon())


def test_video_follow_stopping() -> None:
    """
    test
    """
    detector = ColorDetector()
    tracker = Tracker()

    # Ruta del archivo .avi
    archivo_mp4 = 'data/videos/samples/brass_3.mp4'
    cap = cv2.VideoCapture(archivo_mp4)
    # Verificar si se abrió correctamente
    if not cap.isOpened():
        print("Error al abrir el archivo de video.")
        exit()

    # Bucle de imagenes
    while True:
        # Leer un cuadro del video
        ret, frame = cap.read()
        # Si no se puede leer un cuadro, terminamos
        if not ret:
            print("Fin del video.")
            break

        pieces = detector.detect(frame)
        tracker.update(pieces)
        tracker.draw(frame)

        # Mostrar el cuadro
        cv2.imshow('Video', frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        key = input()
        if key == 's':
            cv2.imwrite('data/images/samples/photo.png', frame)
    cap.release()
    cv2.destroyAllWindows()


def test_video_follow() -> None:
    """
    test
    """
    detector = ColorDetector()
    tracker = Tracker()

    # Ruta del archivo .avi
    archivo_mp4 = 'data/videos/samples/full_video_5.mp4'
    cap = cv2.VideoCapture(archivo_mp4)
    # Verificar si se abrió correctamente
    if not cap.isOpened():
        print("Error al abrir el archivo de video.")
        exit()

    # Bucle de imagenes
    while True:
        # Leer un cuadro del video
        ret, frame = cap.read()
        # Si no se puede leer un cuadro, terminamos
        if not ret:
            print("Fin del video.")
            break

        pieces = detector.detect(frame, verbose=False)
        tracker.update(pieces)
        tracker.draw(frame)

        # Mostrar el cuadro
        cv2.imshow('Video', frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.08)
    cap.release()
    cv2.destroyAllWindows()



def main():
    """
    main
    """
    # test_image_follow()
    # test_video_follow_stopping()
    test_video_follow()


if __name__ == '__main__':
    main()