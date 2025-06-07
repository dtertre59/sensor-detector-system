"""
Detector
utils.py
"""

import numpy as np
import cv2

from src import utils as ut


# Reduce noise
def reduce_noise(image: np.ndarray, ksize: tuple = (31, 31)) -> np.ndarray:
    """
    Reduce noise in the image using Gaussian blur.

    Args:
        image (np.ndarray): The input image.
        ksize (tuple): size. 

    Returns:
        np.ndarray: The denoised image.
    """
    # Apply Gaussian blur to reduce noise
    denoised_image = cv2.GaussianBlur(image, ksize, 0)
    return denoised_image


# Delete small labels
def delete_small_labels(thresh_image: np.ndarray, min_area: int = 135, verbose: bool = True) -> np.ndarray:
    """
    Delete small labels

        Args:
            thresh_image (np.ndarray): The input image.
            min_area (int): The minimum area.

        Returns:
            np.ndarray: The filtered image."""
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh_image)
    # Shoe the number of detected objects
    if verbose:
        print(f'Number of detected ogjects: {num_labels - 1}')  # Rest the background
    # Create a new image for large components
    filtered_image = np.zeros_like(thresh_image)

    # Filter small components
    for label in range(1, num_labels):  # Skip the background (label 0)
        area = stats[label, cv2.CC_STAT_AREA]
        if area >= min_area:
            if verbose:
                print(f'Object {label} Area:', area)
            # If the area is greater than the threshold, keep the component
            filtered_image[labels == label] = 255  # Assign the white value to the large components
    return filtered_image


# Segment image to binary
def segment(gray_image: np.ndarray, min_area: int = 135,
            flat_field: np.ndarray = None, verbose: bool = False) -> np.ndarray:
    """
    segment Image

    Mode 1
    """

    if flat_field is not None:
        difference = cv2.absdiff(gray_image, flat_field)
        # Threshold
        thresh = 20
        _, threshold = cv2.threshold(difference, thresh, 255, cv2.THRESH_BINARY)
    else:
        # binary threshold Manual setting the threshold
        thresh = 85
        _, threshold = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_BINARY)

        # # Apply binary threshold Automatic
        # thresh = 0
        # _, threshold = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_OTSU)

    # ut.show_image(threshold)
    # threshold_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 5)

    # reverse
    # inverted_thresh = cv2.bitwise_not(thresh)

    # Delete small labels
    threshold = delete_small_labels(threshold, min_area, verbose)

    return threshold

# def segment_image_m1(gray_image: np.ndarray) -> np.ndarray:
#     """
#     segment Image

#     Mode 1
#     """
#     # Apply binary threshold
#     _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#     # reverse
#     # Invertir la imagen (objetos en blanco, fondo en negro)
#     inverted_thresh = cv2.bitwise_not(thresh)

#     # Method 1
#     # Encontrar los componentes conectados
#     num_labels, labels = cv2.connectedComponents(inverted_thresh)
#     # Mostrar la cantidad de objetos detectados
#     print(f'Número de objetos detectados: {num_labels - 1}')  # Restamos 1 para ignorar el fondo
#     # Opcional: Colorear cada componente en una imagen de salida
#     output = cv2.cvtColor(inverted_thresh, cv2.COLOR_GRAY2BGR)
#     colors = np.random.randint(0, 255, size=(num_labels, 3), dtype=int)
#     for label in range(1, num_labels):  # Saltamos el fondo
#         output[labels == label] = colors[label]

#     # Method 2
#     # Encontrar contornos (ignorando los agujeros)
#     contornos, _ = cv2.findContours(inverted_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     # Contar los contornos encontrados
#     num_objetos = len(contornos)
#     print(f'Número de objetos detectados: {num_objetos}')
#     # Opcional: Dibujar los contornos sobre la imagen original
#     imagen_con_contornos = cv2.cvtColor(inverted_thresh, cv2.COLOR_GRAY2BGR)
#     # Encontrar el contorno con mayor área
#     contorno_mas_grande = max(contornos, key=cv2.contourArea)
#     cv2.drawContours(imagen_con_contornos, [contorno_mas_grande], -1, (0, 255, 0), 2)
#     # Crear una máscara negra del mismo tamaño que la imagen binaria
#     mascara = np.zeros_like(inverted_thresh)
#     # Dibujar el contorno más grande en blanco en la máscara
#     cv2.drawContours(mascara, [contorno_mas_grande], -1, 255, thickness=cv2.FILLED)
#     # Poner todo lo que está fuera del contorno a negro
#     b = inverted_thresh.copy()
#     b[mascara == 0] = 0

#     return b


def get_mean_color_from_image(image: np.ndarray, original_image: np.ndarray) -> tuple:
    """
    Calculate the mean color of the object in the image.

    Args:
        image (np.ndarray): The binary mask image with the object in white and background in black.
        original_image (np.ndarray): The original color image.

    Returns:
        tuple: The mean color in BGR format.
    """
    # Ensure the binary mask is binary (0 and 255)
    _, binary_mask = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # Create a mask where white pixels in the binary mask (value 255) are True
    mask = binary_mask == 255

    # Apply the mask to the original image to select the relevant pixels
    selected_pixels = original_image[mask]

    # Calculate the mean color (in BGR)
    mean_color = np.mean(selected_pixels, axis=0)
    return tuple(map(int, mean_color))


def get_mean_color_from_label(label: int, labels: np.ndarray, image: np.ndarray) -> tuple[int, int, int]:
    """
    Get the mean color of a region in the image specified by the label.

    Args:
        label (int): The label of the region.
        labels (np.ndarray): The labeled image.
        image (np.ndarray): The original image.

    Returns:
        tuple: The mean color of the region as a tuple of three integers (B, G, R).
    """
    # Create a mask for the region with the specified label
    mask = (labels == label).astype(np.uint8)

    # Calculate the mean color of the region in the original image
    mean_color = cv2.mean(image, mask=mask)[:3]  # Ignore the alpha channel if present

    # Convert the mean color to integers
    mean_color = tuple(map(int, mean_color))

    return mean_color


def get_gravity_center(image: np.ndarray) -> tuple:
    """
    Calculate the gravity center (centroid) of the object in the image.

    Args:
        image (np.ndarray): The binary mask image with the object in white and background in black.

    Returns:
        tuple: The (x, y) coordinates of the gravity center.
    """
    # Calculate moments of the binary image
    moments = cv2.moments(image)

    # Calculate x, y coordinate of center
    if moments["m00"] != 0:
        cX = int(moments["m10"] / moments["m00"])
        cY = int(moments["m01"] / moments["m00"])
    else:
        cX, cY = 0, 0

    return (cX, cY)
