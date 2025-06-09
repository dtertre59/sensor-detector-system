"""
utils.py
"""

import os
from pathlib import Path
import cv2
import numpy as np


def delta_e(a1: np.ndarray, a2: np.ndarray) -> float:
    """
    Computes the Euclidean distance (ΔE) between two vectors

    Args:
        a1 (np.ndarray): First vector.
        a2 (np.ndarray): Second vector.

    Returns:
        float: The Euclidean distance between the two input vectors.
    """
    return float(np.linalg.norm(a1.astype(float) - a2.astype(float)))


def bgr_to_lab(bgr_color: tuple[int, int, int]) -> tuple[int, int, int]:
    """
    Convert a BGR color to LAB color space.

    Args:
        bgr_color (tuple[int, int, int]): The BGR color as a tuple.

    Returns:
        tuple[int, int, int]: The LAB color as a tuple.
    """
    bgr_array = np.uint8([[bgr_color]])
    lab_color = cv2.cvtColor(bgr_array, cv2.COLOR_BGR2Lab)[0][0]
    return tuple(map(int, lab_color))


def show_image(image):
    """
    show image
    """
    cv2.imshow('Test image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_directory_filepaths(directory: Path) -> list[Path]:
    """
    get_directory_filenames
    """
    try:
        # Listar los archivos en el directorio
        filepaths = [Path(os.path.join(directory, f)).resolve() for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return filepaths
    except FileNotFoundError:
        print("Directory is not found.")
        return []
    except PermissionError:
        print("You dont have access.")
        return []


def obtain_filenames_last_number(directory: Path, name: str, verbose: bool = False) -> int:
    """
    Obtain last number
    """
    filenames = os.listdir(directory)
    if verbose:
        print('Directory:', directory)
        print('Name:', name)
        print(filenames)
    numbers = [int(filename.split('_')[-1].split('.')[0]) for filename in filenames if filename.startswith(f'{name}_')]
    if verbose:
        print(numbers)
    if not numbers:
        return 0
    return max(numbers)


def get_distance(p1: tuple, p2: tuple) -> float:
    """
    get distance
    """
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5