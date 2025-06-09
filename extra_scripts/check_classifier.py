
"""
Check segmentation
"""

import cv2

from src.detector.color_detector import ColorDetector
from src.classifier import LabClassifier
from src.utils import bgr_to_lab


# Color: (124, 123, 132) {<MaterialEn.COPPER: 0>: 19.1049731745428, <MaterialEn.ZINC: 1>: 4.47213595499958, <MaterialEn.BRASS: 2>: 21.587033144922902, <MaterialEn.PCB: 3>: 6.708203932499369}
# Color: (125, 123, 133) {<MaterialEn.COPPER: 0>: 18.439088914585774, <MaterialEn.ZINC: 1>: 5.0, <MaterialEn.BRASS: 2>: 20.615528128088304, <MaterialEn.PCB: 3>: 5.830951894845301}


def loop(detector: ColorDetector, image):
    """ main loop """
    _, pieces = detector.detect(image, merge_pieces=False)

    for piece in pieces:
        piece_mean_color_bgr = piece.calculate_mean_color()
        piece_mean_color_lab = bgr_to_lab(piece_mean_color_bgr)
        material, dist = LabClassifier.which_material(piece_mean_color_lab, verbose=True)
        piece.name = f'{material.name.lower()}'
        piece.draw(image)

    return image


def main() -> None:
    """
    Main function to check segmentation.
    """
    detector = ColorDetector(thresh=80, min_area=1000)
    # detector.flat_field = cv2.imread('data/images/background/background_1.png')

    image_paths = [
        'data/images/dataset_4/copper/copper_1.png',
        'data/images/dataset_4/brass/brass_1.png',
        'data/images/dataset_4/zinc/zinc_1.png',
        'data/images/dataset_4/pcb/pcb_1.png',
    ]
    # for i in range(0, 1):
    #     image_path.append(f'data/images/samples/sequence/sequence_sample_1/sample_{i}.png')
    
    for image_path in image_paths:
        image = cv2.imread(image_path)  # BGR format image
        loop(detector, image)
        cv2.imshow('Video', image)
        cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
