"""
Colors practical

"""
import numpy as np

from src.utils import delta_e, bgr_to_lab


MATERIALS_BGR = {
    'copper': (83, 105, 136),
    'zinc': (135, 140, 142),
    'brass': (80, 123, 140),
    'pcb': (101, 123, 117)

}


def material_similarity_lab(color_lab: tuple, verbose: bool = False) -> tuple:
    """
    mat
    """
    material = None
    last_de = None

    if verbose:
        print('Lab color to Compare', color_lab)

    for material_name, material_color_bgr in MATERIALS_BGR.items():
        material_color_lab = bgr_to_lab(material_color_bgr)
        de = delta_e(np.array(material_color_lab[1:]), np.array(color_lab[1:]))  # dont use luminosity

        if verbose:
            print('Comparation with material', material_name, 'lab color', material_color_lab, 'Sim', de)

        if material is None:
            material = material_name
        else:
            material = material_name if de < last_de else material

        if last_de is None:
            last_de = de
        else:
            last_de = de if de < last_de else last_de

    return material, last_de


def main():
    """
    Main function to run the color detection script.
    """
    # Define the BGR colors for copper, zinc, and brass
    copper_bgr = MATERIALS_BGR['copper']
    zinc_bgr = MATERIALS_BGR['zinc']
    brass_bgr = MATERIALS_BGR['brass']
    pcb_bgr = MATERIALS_BGR['pcb']

    # Pieces mean colors
    my_mean_color_copper_1 = (86, 106, 133)     # darker copper
    my_mean_color_copper_2 = (93, 127, 154)     # lighter copper

    my_mean_color_brass_1 = (78, 120, 137)  # darker brass
    my_mean_color_brass_2 = (87, 125, 138)  # lighter brass

    # COPPER Convert BGR to LAB
    copper_lab = bgr_to_lab(copper_bgr)
    print('COPPER (LAB)', copper_lab)
    my_mean_color_copper_lab_1 = bgr_to_lab(my_mean_color_copper_1)
    print(my_mean_color_copper_lab_1)
    my_mean_color_copper_lab_2 = bgr_to_lab(my_mean_color_copper_2)
    print(my_mean_color_copper_lab_2)

    # BRASS Convert BGR to LAB
    brass_lab = bgr_to_lab(brass_bgr)
    print('BRASS (LAB)', brass_lab)
    my_mean_color_brass_lab_1 = bgr_to_lab(my_mean_color_brass_1)
    print(my_mean_color_brass_lab_1)
    my_mean_color_brass_lab_2 = bgr_to_lab(my_mean_color_brass_2)
    print(my_mean_color_brass_lab_2)

    # ZINC
    zinc_lab = bgr_to_lab(zinc_bgr)
    print('ZINC (LAB)', zinc_lab)

    # PCB
    pcb_lab = bgr_to_lab(pcb_bgr)
    print('PCB (LAB)', pcb_lab)

    # Similarity
    print('SIMILARITY')
    print(material_similarity_lab(my_mean_color_copper_lab_2, verbose=True))
    print(material_similarity_lab(my_mean_color_brass_lab_2, verbose=True))


if __name__ == '__main__':
    main()
