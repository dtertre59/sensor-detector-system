"""
utils.py
"""

import os
from pathlib import Path
import cv2


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
    

def obtain_filenames_last_number(directory: Path, name: str) -> int:
    """
    Obtain last number
    """
    filenames = os.listdir(directory)
    numbers = [int(filename.split('_')[-1].split('.')[0]) for filename in filenames if filename.startswith(f'{name}_')]
    if not numbers:
        return 0
    return max(numbers)
