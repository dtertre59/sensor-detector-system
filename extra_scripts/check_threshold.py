
"""
Check segmentation
"""

import cv2

from src.detector.color_detector import ColorDetector


def main() -> None:
    """
    Main function to check segmentation.
    """
    detector = ColorDetector(thresh=80, min_area=1000)
    # detector.flat_field = cv2.imread('data/images/background/background_1.png')

    image_paths = [
        'data/images/dataset_4/copper/copper_1.png',
        'data/images/dataset_4/brass/brass_1.png',
    ]
    # for i in range(0, 1):
    #     image_path.append(f'data/images/samples/sequence/sequence_sample_1/sample_{i}.png')
    
    for image_path in image_paths:
        image = cv2.imread(image_path)

        t_i, _ = detector.detect(image, merge_pieces=False)
        t_i = cv2.cvtColor(t_i, cv2.COLOR_GRAY2BGR)
        cv2.imshow('Video', cv2.vconcat([image, t_i]))
        cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
