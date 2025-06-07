
"""
Check segmentation
"""

import cv2

from src.detector.color_detector import ColorDetector


def main() -> None:
    """
    Main function to check segmentation.
    """
    detector = ColorDetector(min_area=1000)
    # detector.flat_field = cv2.imread('data/images/background/background_1.png')

    for i in range(0, 13):
        print(i)
        image_path = f'data/images/samples/sequence/sequence_sample_1/sample_{i}.png'
        image = cv2.imread(image_path)

        t_i, pieces = detector.detect(image)
        cv2.imshow('Video', cv2.vconcat([image, t_i]))
        cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
