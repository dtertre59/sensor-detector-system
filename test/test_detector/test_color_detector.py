"""
test_color_detector.py
"""

import numpy as np
from pathlib import Path
import cv2
from cv2.typing import MatLike

# from src.detector.base_detector import DetectorException
from src.detector.color_detector import ColorDetector

from src.utils import show_image

# BGR FORMAT
ZINC_COLOR = (200, 196, 186)
BRASS_COLOR = (110, 193, 225)
COPPER_COLOR = (51, 87, 255)


def recorte_imagen(image, x, y, w, h):
    """
    recorte_imagen
    """
    return image[y:y + h, x:x + w]

def compare_colors(colors: list[tuple]) -> None:
    """
    Compare colors
    """
    # Dimensiones de cada bloque de color
    ancho_bloque = 50
    alto_bloque = 50

    # Crear una imagen para contener todos los colores (en una fila)
    ancho_imagen = ancho_bloque * len(colors)
    alto_imagen = alto_bloque
    imagen = np.zeros((alto_imagen, ancho_imagen, 3), dtype=np.uint8)

    # Dibujar cada color en la imagen
    for i, color in enumerate(colors):
        inicio_x = i * ancho_bloque
        fin_x = inicio_x + ancho_bloque
        imagen[:, inicio_x:fin_x] = color

    # Mostrar la imagen
    cv2.imshow('Colores', imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def mode1():
    # Crop image
    image_croped = recorte_imagen(image, int(640/3), int(640/3), int(640/3), int(640/3))
    # Blurred image
    image_blurred = cv2.GaussianBlur(image_croped, (21, 21), 0)

    # Uniform image
    # Obtener el color promedio
    mean_color = cv2.mean(image_blurred)[:3]
    print('Mean color:', mean_color)
    # Crear una imagen del mismo tamaño con el color promedio
    uniform_image = np.full(image_blurred.shape, mean_color, dtype=np.uint8)
    # Show image
    show_image(image_blurred)
    show_image(uniform_image)


def mode2():
    # Crop image
    image_croped = recorte_imagen(image, int(640/3), int(640/3), int(640/3), int(640/3))
    # Blurred image
    image_blurred = cv2.medianBlur(image_croped, 5)

    # Show image
    show_image(image_blurred)


def grabcut_algorithm(image):
    # Crear una máscara de ceros (toda la imagen se considera fondo inicialmente)
    mask = np.zeros(image.shape[:2], np.uint8)

    # Crear modelos de fondo y primer plano (son necesarios como parámetros en grabCut)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # Definir el rectángulo (bounding box) que cubre el objeto de interés
    # El rectángulo debe ser de la forma (x, y, ancho, alto)
    rect = (50, 50, 400, 400)  # Ejemplo: (x=50, y=50, width=400, height=400)

    # Aplicar grabCut
    cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    # Modificar la máscara: valores 0 y 2 se consideran fondo (0), y 1 y 3 se consideran primer plano (1)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Obtener la image segmentada usando la máscara
    image_segmentada = image * mask2[:, :, np.newaxis]

    # Mostrar la image segmentada
    cv2.imshow('image Segmentada', image_segmentada)

    # Esperar hasta que se presione una tecla y luego cerrar las ventanas
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def mode3_segment():
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    # opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations=1)
    # Aplicar la operación de apertura para eliminar puntos aislados

    # sure background area
    sure_bg = cv2.dilate(thresh, kernel, iterations=1)

    pixel_medio = calcular_pixel_medio(sure_bg)
    print(pixel_medio)
    # Dibujar un círculo en el punto medio
    cv2.circle(image, pixel_medio, radius=5, color=(255,255,255), thickness=-1)  # Círculo blanco (255)
    show_image(image)
    show_image(thresh)
    # show_image(opening)
    show_image(sure_bg)

    ######################

    # grabcut_algorithm(image)

    #####################

    #imagen
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

    # Crear una imagen del mismo tamaño con el color promedio
    uniform_image = np.full(original_image.shape, mean_color, dtype=np.uint8)
    show_image(uniform_image)


def reduce_noise(image: np.ndarray) -> np.ndarray:
    """
    Reduce noise in the image using Gaussian blur.

    Args:
        image (np.ndarray): The input image in grey scale.

    Returns:
        np.ndarray: The denoised image.
    """
    # Apply Gaussian blur to reduce noise
    denoised_image = cv2.GaussianBlur(image, (31, 31), 0)
    return denoised_image


def segment_image_m1(image: MatLike) -> MatLike:
    """
    segment Image

    Mode 1
    """
    # reduce noice
    image = reduce_noise(image)
    # gray image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply binary threshold
    _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # reverse
    # Invertir la imagen (objetos en blanco, fondo en negro)
    inverted_thresh = cv2.bitwise_not(thresh)

    # Method 1
    # Encontrar los componentes conectados
    num_labels, labels = cv2.connectedComponents(inverted_thresh)
    # Mostrar la cantidad de objetos detectados
    print(f'Número de objetos detectados: {num_labels - 1}')  # Restamos 1 para ignorar el fondo
    # Opcional: Colorear cada componente en una imagen de salida
    output = cv2.cvtColor(inverted_thresh, cv2.COLOR_GRAY2BGR)
    colors = np.random.randint(0, 255, size=(num_labels, 3), dtype=int)
    for label in range(1, num_labels):  # Saltamos el fondo
        output[labels == label] = colors[label]

    # Method 2
    # Encontrar contornos (ignorando los agujeros)
    contornos, _ = cv2.findContours(inverted_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Contar los contornos encontrados
    num_objetos = len(contornos)
    print(f'Número de objetos detectados: {num_objetos}')
    # Opcional: Dibujar los contornos sobre la imagen original
    imagen_con_contornos = cv2.cvtColor(inverted_thresh, cv2.COLOR_GRAY2BGR)
    # Encontrar el contorno con mayor área
    contorno_mas_grande = max(contornos, key=cv2.contourArea)
    cv2.drawContours(imagen_con_contornos, [contorno_mas_grande], -1, (0, 255, 0), 2)
    # Crear una máscara negra del mismo tamaño que la imagen binaria
    mascara = np.zeros_like(inverted_thresh)
    # Dibujar el contorno más grande en blanco en la máscara
    cv2.drawContours(mascara, [contorno_mas_grande], -1, 255, thickness=cv2.FILLED)
    # Poner todo lo que está fuera del contorno a negro
    b = inverted_thresh.copy()
    b[mascara == 0] = 0

    return b

def reduce_contourns(image: MatLike, max_contourns: int = -1) -> MatLike:
    pass

def delete_all_contourns_except_1(image: MatLike):
    # Encontrar contornos (ignorando los agujeros)
    contornos, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Contar los contornos encontrados
    num_objetos = len(contornos)
    print(f'Número de objetos detectados: {num_objetos}')
    # Opcional: Dibujar los contornos sobre la imagen original
    imagen_con_contornos = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # Encontrar el contorno con mayor área
    contorno_mas_grande = max(contornos, key=cv2.contourArea)
    cv2.drawContours(imagen_con_contornos, [contorno_mas_grande], -1, (0, 255, 0), 2)
    # Crear una máscara negra del mismo tamaño que la imagen binaria
    mascara = np.zeros_like(image)
    # Dibujar el contorno más grande en blanco en la máscara
    cv2.drawContours(mascara, [contorno_mas_grande], -1, 255, thickness=cv2.FILLED)
    # Poner todo lo que está fuera del contorno a negro
    b = image.copy()
    b[mascara == 0] = 0
    return b


def get_mean_color_from_image(image: MatLike, original_image: MatLike) -> tuple:
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


def which_material(mean_color: tuple) -> str:
    """
    Determine the material based on the mean color.

    Args:
        mean_color (tuple): The mean color in BGR format.

    Returns:
        str: The name of the material.
    """
    # Define reference colors for different materials (in BGR format)
    reference_colors = {
        "copper": COPPER_COLOR,
        "zinc": ZINC_COLOR,
        "brass": BRASS_COLOR,
        # Add more materials and their reference colors here
    }

    # Calculate the Euclidean distance between the mean color and each reference color
    distances = {material: np.linalg.norm(np.array(mean_color) - np.array(color)) for material, color in reference_colors.items()}

    # Find the material with the smallest distance
    closest_material = min(distances, key=distances.get)

    return closest_material


# ----- DEF GOOD TESTING ----- #


def test_detect_function(image: MatLike):
    """
    test
    """
    detector = ColorDetector(min_area=600)
    detector.initialize()
    pieces = detector.detect(image)

    for piece in pieces:
        print(piece)
        piece.draw(image, track=False)

    show_image(image)



def main() -> None:
    """
    main
    """
    filename = r'data/images/samples/cobre_2.jpeg'
    # filename = r'data/images/samples/zinc_1.jpeg'
    # filename = r'data/images/samples/laton_1.jpeg'
    if Path(filename).exists():
        print('File exists')
    else:
        print('File does not exist')
        raise FileNotFoundError('File does not exist')
    path = Path(filename).resolve()

    image = cv2.imread(filename)
    # Resize image
    image = cv2.resize(image, (640, 640))

    # segment_image = segment_image_m1(image)
    # show_image(segment_image)

    # # gravity_center = get_gravity_center(segment_image)
    # # print('Gravity center:', gravity_center)
    # mean_color = get_mean_color_from_image(segment_image, image)
    # print('Material mean color', mean_color)
    # uniform_image = np.full(image.shape, mean_color, dtype=np.uint8)
    # show_image(uniform_image)
    # compare_colors([ZINC_COLOR, BRASS_COLOR, COPPER_COLOR, mean_color])

    # print(which_material(mean_color))

    # GOOD TESTING
    test_detect_function(image)


main()