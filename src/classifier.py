"""
Classfiers
"""

from enum import Enum, auto

import numpy as np

from src import utils as ut


class MaterialEn(Enum):
    """
    Materials Enumerator
    """
    COOPER = 0
    ZINC = auto()
    BRASS = auto()
    PCB = auto()


class BgrClassifier:
    """
    BGR Classifer [B, G, R]

    B = Blue 
    G = Green
    R = Red
    """
    MATERIALS_BGR_COLORS = {
        # Dataset 1
        # 'zinc': (200, 196, 186),
        # 'brass': (110, 193, 225),
        # 'copper': (51, 87, 255),

        # # Dataset 2
        # "copper": (152, 180, 210),
        # "zinc": (203, 209, 211),
        # "brass": (157, 199, 213),
        # "pcb": (183, 204, 192),

        # # Dataset 3
        # "copper": (81,103,137),
        # "zinc": (125,131,133),
        # "brass": (83,125,142),
        # "pcb": (101,123,111)

        # # Dataset 4
        # "copper": (83, 105, 136),
        # "zinc": (135, 140, 142),
        # "brass": (80, 123, 140),
        # "pcb": (80, 123, 140)

        # Manual
        MaterialEn.COOPER: (83, 105, 136),
        MaterialEn.ZINC: (135, 140, 142),
        MaterialEn.BRASS: (80, 123, 140),
        MaterialEn.PCB: (101, 123, 117)
    }

    @staticmethod
    def which_material(color_rgb: tuple[int, int, int]) -> tuple[MaterialEn, float]:
        """
        which material it is 
        """
        euclidean_distances_dict = {material: np.linalg.norm(np.array(color_rgb) - np.array(m_color))
                                    for material, m_color in BgrClassifier.MATERIALS_BGR_COLORS.items()}
        # Find the material with the smallest distance
        closest_material = min(euclidean_distances_dict, key=euclidean_distances_dict.get)

        dist = euclidean_distances_dict[closest_material]
        return closest_material, dist


class LabClassifier:
    """
    LAB Classifer [L, a, b]

    L = Lightness
    a = a-axis (Green<->Red)
    b = -axis (Blue<->Yellow)
    """

    MATERIALS_LAB_COLORS = {
        # Manual
        MaterialEn.COOPER: (120, 137, 145),
        MaterialEn.ZINC: (135, 140, 142),
        MaterialEn.BRASS: (133, 128, 154),
        MaterialEn.PCB: (101, 123, 117)
    }

    @staticmethod
    def which_material(color_lab: tuple[int, int, int], use_lightness: bool = False) -> tuple[MaterialEn, float]:
        """
        which material it is, using LAB FORMAT
        """
        if use_lightness:
            euclidean_distances_dict = {material_name: ut.delta_e(np.array(color_lab), np.array(m_color)) 
                                        for material_name, m_color in LabClassifier.MATERIALS_LAB_COLORS.items()}
        else:
            euclidean_distances_dict = {material_name: ut.delta_e(np.array(color_lab[1:]), np.array(m_color[1:])) 
                                        for material_name, m_color in LabClassifier.MATERIALS_LAB_COLORS.items()}

        # Find the material with the smallest distance
        closest_material = min(euclidean_distances_dict, key=euclidean_distances_dict.get)
        dist = euclidean_distances_dict[closest_material]
        return closest_material, dist


if __name__ == '__main__':
    color = (140, 133, 150)     # LAB format
    material, distance = LabClassifier.which_material(color)
    a = print(material.name, distance)
