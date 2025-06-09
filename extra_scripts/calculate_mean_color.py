"""
In this script, we calculate the mean color of the images in the dataset.
The mean color is calculated by cropping the image and blurring it.
The blurred image is used to calculate the mean color.
"""
import os
from pathlib import Path

import cv2
import numpy as np
import json

from src.classifier import MaterialEn

from src.detector.color_detector import ColorDetector
from src.utils import get_directory_filepaths, show_image


def export_mean_colors(mean_colors: dict[str, tuple[int, int, int]], output_file: str):
    """
    Export the mean colors to a JSON file.

    Args:
        mean_colors (dict[str, tuple[int, int, int]]): The mean colors dictionary.
        output_file (str): The output file path.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mean_colors, f, indent=4)


def get_directories_filepaths(directories: list[Path]) -> list[list[Path]]:
    """
    get_directories_filepaths
    """
    directories_filepaths = []
    for directory in directories:   
        filepaths = get_directory_filepaths(directory)
        directories_filepaths.append(filepaths)
    return directories_filepaths


def calculate_mean_color(mean_colors: list[tuple]) -> tuple[int, int, int]:
    """
    calculate_mean_color

    BGR and LAB colors are calculated as the mean of the colors in the list.
    """
    red = green = blue = 0
    for color in mean_colors:
        red += color[0]
        green += color[1]
        blue += color[2]
    final_red = red // len(mean_colors)
    final_green = green // len(mean_colors)
    final_blue = blue // len(mean_colors)
    final_color = (int(final_red), int(final_green), int(final_blue))
    return final_color


def get_bgr_mean_color_for_image(image_filename: Path) -> tuple[int, int, int]:
    """
    get_mean_color
    """
    detector = ColorDetector(thresh=80)
    # 1. Load image
    image = cv2.imread(str(image_filename))

    threshold_image, _ = detector.detect(image)

    # imagen
    original_image = image.copy()

    # Crear una máscara donde los píxeles negros en la binaria (valor 0) sean True
    mask = threshold_image == 255  # Los píxeles negros son True

    # Aplicar la máscara a la imagen original para seleccionar los píxeles relevantes
    selected_pixels = original_image[mask]  # Extrae los píxeles correspondientes a los negros

    # Calcular la media de los colores (en BGR)
    mean_color = np.mean(selected_pixels, axis=0)
    return mean_color


def get_lab_mean_color_for_image(image_filename: Path) -> tuple[int, int, int]:
    """
    get_mean_color
    """
    # vars
    detector = ColorDetector(thresh=80)

    # 1. Load image
    image = cv2.imread(str(image_filename))

    threshold_image, _ = detector.detect(image)

    # LAB format
    original_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)

    # Crear una máscara donde los píxeles negros en la binaria (valor 0) sean True
    mask = threshold_image == 255  # Los píxeles negros son True

    # Aplicar la máscara a la imagen original para seleccionar los píxeles relevantes
    selected_pixels = original_image[mask]  # Extrae los píxeles correspondientes a los negros

    # Calcular la media de los colores
    mean_color = np.mean(selected_pixels, axis=0)
    return mean_color


def get_mean_color_from_images(dataset: int, material: Path, image_filenames: list[Path], image_format: str = 'bgr') -> tuple[int, int, int]:
    """
    get_mean_color_from_images
    """
    try:
        os.mkdir(f'data/generated/dataset_{dataset}')
        os.mkdir(f'data/generated/dataset_{dataset}/mean_colors')
    except:
        pass
    file = open(f'data/generated/dataset_{dataset}/mean_colors/{material}.csv', 'w', encoding='utf-8')
    file.write("image_filename;mean_color_red;mean_color_green;mean_color_blue\n")
    images_mean_colors: list[tuple] = []

    for image_filename in image_filenames:
        # print(image_filename)
        if image_format == 'bgr':
            image_mean_color = get_bgr_mean_color_for_image(image_filename)
        elif image_format == 'lab':
            image_mean_color = get_lab_mean_color_for_image(image_filename)
        else:
            raise ValueError("Unsupported image format. Use 'bgr' or 'lab'.")

        images_mean_colors.append(image_mean_color)
        file.write(f"{image_filename.stem};{image_mean_color[0]};{image_mean_color[1]};{image_mean_color[2]}\n")
    file.close()

    final_mean_color = calculate_mean_color(images_mean_colors)
    return final_mean_color


def main():
    """
    main
    """

    # VARS
    dataset = 4
    image_formats = ['bgr', 'lab']  # 'bgr' or 'lab'

    # 1. Get filenames from all images in the dataset
    materials = [material.name.lower() for material in MaterialEn]
    print('Materials:', materials)

    directories: list[Path] = []
    for material in materials:
        directories.append(Path(f'data/images/dataset_{dataset}/{material}'))

    # Get the file paths for each material directory
    materials_images_filenames: list[list[Path]] = get_directories_filepaths(directories)

    # 2. For each image, calculate the mean color
    materials_mean_colors_dict = {image_format: {} for image_format in image_formats}

    for image_format in image_formats:
        for index, material_images_filenames in enumerate(materials_images_filenames):
            material_mean_color = get_mean_color_from_images(dataset, materials[index], material_images_filenames,
                                                             image_format=image_format)
            materials_mean_colors_dict[image_format][materials[index]] = tuple(material_mean_color)

    export_mean_colors(materials_mean_colors_dict, f'data/generated/dataset_{dataset}/mean_colors.json')
    print(materials_mean_colors_dict)


if __name__ == '__main__':
    main()
