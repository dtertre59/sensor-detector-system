import cv2


import src.utils as ut
import src.detector.utils as dut


def test_1_delete_background():
    """
    Test
    """
    background = cv2.imread('data/images/background/background_0.png')
    image = cv2.imread('data/images/sample_147.png')
    print(background.shape)
    print(image.shape)
    ut.show_image(image)

    # Reduce noise
    noise_free_background = dut.reduce_noise(background, (31, 31))
    noise_free_image = dut.reduce_noise(image, (31, 31))
    ut.show_image(noise_free_image)

    # Convert to gray
    gray_background = cv2.cvtColor(noise_free_background, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.cvtColor(noise_free_image, cv2.COLOR_BGR2GRAY)
    ut.show_image(gray_image)

    # Delete background
    # Restar las imágenes (el fondo se cancela)
    difference = cv2.absdiff(gray_image, gray_background)
    ut.show_image(difference)

    # Threshold
    thresh = 15
    _, threshold = cv2.threshold(difference, thresh, 255, cv2.THRESH_BINARY)
    ut.show_image(threshold)

    # Group pixels
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
    ut.show_image(threshold)


test_1_delete_background()