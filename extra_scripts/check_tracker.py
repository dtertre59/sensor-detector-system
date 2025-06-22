
"""
Check segmentation
"""

import time

import cv2
import numpy as np

from src.detector.color_detector import ColorDetector
from src.tracker import Tracker
from src.classifier import LabClassifier
from src.utils import bgr_to_lab


def loop(detector: ColorDetector, tracker: Tracker, image: np.ndarray) -> np.ndarray:
    """ main loop """
    threshold_image, pieces = detector.detect(image, merge_pieces=False)

    # for piece in pieces:
    #     piece_mean_color_bgr = piece.calculate_mean_color()
    #     piece_mean_color_lab = bgr_to_lab(piece_mean_color_bgr)
    #     material, dist = LabClassifier.which_material(piece_mean_color_lab, verbose=True)
    #     piece.name = f'{material.name.lower()}'
    #     piece.draw(threshold_image)

    # Track pieces
    _ = tracker.update(pieces, verbose=True)

    t_i = cv2.cvtColor(threshold_image, cv2.COLOR_GRAY2BGR)
    tracker.draw(image, track=True)

    final_image = cv2.vconcat([image, t_i])

    return final_image


def main() -> None:
    """
    Main function to check segmentation.
    """

    # ----- vars ----- #

    # Window
    window_name = 'Full Screen Tracker'
    # cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    # # Full screen mode
    # cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Detector
    detector = ColorDetector(thresh=80, min_area=300)  # pi config
    # detector = ColorDetector(thresh=140, min_area=300)      # bad config
    # detector.flat_field = cv2.imread('data/images/background/background_1.png')

    # Tracker
    tracker = Tracker(min_area=300)

    # ----- with secuence of images ----- #

    # image_paths = [
    #     'data/images/dataset_4/copper/copper_1.png',
    #     'data/images/dataset_4/brass/brass_1.png',
    #     'data/images/dataset_4/zinc/zinc_1.png',
    #     'data/images/dataset_4/pcb/pcb_1.png',
    # ]

    # for image_path in image_paths:
    #     image = cv2.imread(image_path)  # BGR format image
    #     loop(detector, tracker, image)
    #     cv2.imshow('Video', image)
    #     cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # ----- with video ----- #

    video_mp4 = 'data/videos/samples/full_video_tspeed3_5.mp4'
    cap = cv2.VideoCapture(video_mp4)
    # Verificar si se abrió correctamente
    if not cap.isOpened():
        print("Error opening video file.")
        exit()

    x = 0
    while True:
        x += 1
        
        # Leer un cuadro del video
        ret, image = cap.read()

        if x % 3 == 0:
            continue

        # Si no se puede leer un cuadro, terminamos
        if not ret:
            print("End of video.")
            break

        frame = loop(detector, tracker, image)

        # Mostrar el cuadro
        cv2.imshow('Full Screen Tracker', frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.04)
        input("Press Enter to continue...")


if __name__ == '__main__':
    main()
