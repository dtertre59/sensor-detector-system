"""
In this script, we calculate the mean color of the images in the dataset.
The mean color is calculated by cropping the image and blurring it.
The blurred image is used to calculate the mean color.
"""

from pathlib import Path

import cv2
import numpy as np
import json

from src.utils import get_directory_filepaths


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


def get_mean_color_for_image(image_filename: Path) -> tuple[int, int, int]:
    """
    get_mean_color
    """
    # 1. Load image
    image = cv2.imread(str(image_filename))
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=5)

    # imagen
    original_image = image.copy()
    binary_image = sure_bg.copy()

    # Asegurarse de que la imagen binaria es realmente binaria (0 y 255)
    _, binary_mask = cv2.threshold(binary_image, 127, 255, cv2.THRESH_BINARY)

    # Crear una máscara donde los píxeles negros en la binaria (valor 0) sean True
    mask = binary_mask == 0  # Los píxeles negros son True

    # Aplicar la máscara a la imagen original para seleccionar los píxeles relevantes
    selected_pixels = original_image[mask]  # Extrae los píxeles correspondientes a los negros

    # Calcular la media de los colores (en BGR)
    mean_color = np.mean(selected_pixels, axis=0)
    return mean_color


def get_mean_color_from_images(material: Path, image_filenames: list[Path]) -> tuple[int, int, int]:
    """
    get_mean_color_from_images
    """
    file = open(f'data/generated/dataset_1/mean_colors/{material}.csv', 'w', encoding='utf-8')
    file.write("image_filename;mean_color_red;mean_color_green;mean_color_blue\n")

    images_mean_colors: list[tuple] = []
    for image_filename in image_filenames:
        image_mean_color = get_mean_color_for_image(image_filename)
        images_mean_colors.append(image_mean_color)
        file.write(f"{image_filename.stem};{image_mean_color[0]};{image_mean_color[1]};{image_mean_color[2]}\n")
    file.close()
    return calculate_mean_color(images_mean_colors)


def main():
    """
    main
    """
    # 1. Get filenames from all images in the dataset
    materials = ['copper', 'zinc', 'brass']
    directories: list[Path] = []
    for material in materials:
        directories.append(Path(f'data/images/dataset_1/{material}'))

    materials_images_filenames: list[list[Path]] = get_directories_filepaths(directories)

    # 2. For each image, calculate the mean color
    materials_mean_colors = []
    materials_mean_colors_dict = {}
    for index, material_images_filenames in enumerate(materials_images_filenames):
        material_mean_color = get_mean_color_from_images(materials[index], material_images_filenames)
        materials_mean_colors.append(material_mean_color)
        materials_mean_colors_dict[materials[index]] = material_mean_color
    
    export_mean_colors(materials_mean_colors_dict, 'data/generated/dataset_1/mean_colors.json')
    print(materials_mean_colors)


if __name__ == '__main__':
    main()
