"""
piece.py
"""
from __future__ import annotations

import time
import json
import numpy as np

import cv2

from src.classifier import MaterialEn, LabClassifier
from src.utils import bgr_to_lab


class Piece:
    """
    Class BasePiece to store data about a piece.

    Attributes:
        name (str): The name of the piece.
        category (MaterialEn): The category of the piece.
        bbox (tuple): (x, y, w, h)
        mean_colors (list): A list of dictionaries with mean color and time.
        positions (list): A list of dictionaries with position and time.
        areas (list): A list of dictionaries with area and time.
        speed (tuple): The speed of the piece as a tuple of two numbers (vx, vy).

    Methods:
        add_mean_color: Add a new mean color with the current time.
        calculate_mean_color: Calculate the overall mean color using all mean colors.
        add_position: Add a new position with the current time.
        calculate_speed: Calculate the speed of the piece using the positions and times.
        get_bbox_points: Get bounding box points.
        draw: Draw the piece information on the image.
        update: Update with other piece.
    """

    def __init__(self, id: int, name: str = 'unknown', category: MaterialEn = MaterialEn.UNKNOWN,
                 bbox: tuple | None = None,
                 mean_color: tuple | None = None, position: tuple | None = None, area: int | None = None,
                 speed: float | None = None):
        """
        Initialize a BasePiece instance.

        Args:
            id (int): The id of the piece.
            name (str): The name of the piece.
            category (str): The category of the piece.
            bbox (tuple): (x, y, w, h).
            mean_color (tuple): (B, G, R).
            position (tuple): (x, y).
            area (int): The area of the piece in pixels.
            speed (tuple): The speed of the piece as a tuple of two numbers (vx, vy).
        """

        self._id = id
        self._name = name
        self._category = category
        self._bbox = bbox

        self._mean_colors = []
        if mean_color is not None:
            self.add_mean_color(mean_color)

        self._positions = []
        if position is not None:
            self.add_position(position)

        self._areas = []
        if area is not None:
            self.add_area(area)

        self._speed = speed

    @property
    def id(self) -> str:
        """
        Get the id of the piece.

        Returns:
            int: The id of the piece.
        """
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        """
        Set the id of the piece.

        Args:
            value (int): The id of the piece.

        Raises:
            ValueError: If the id is not an int.
        """
        if not isinstance(value, int):
            raise ValueError("Name must be an int")
        self._id = value

    @property
    def name(self) -> str:
        """
        Get the name of the piece.

        Returns:
            str: The name of the piece.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the piece.

        Args:
            value (str): The name of the piece.

        Raises:
            ValueError: If the name is not a string.
        """
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self._name = value

    @property
    def category(self) -> MaterialEn:
        """
        Get the category of the piece.

        Returns:
            str: The category of the piece.
        """
        return self._category

    @category.setter
    def category(self, value: MaterialEn) -> None:
        """
        Set the category of the piece.

        Args:
            value (str): The category of the piece.

        Raises:
            ValueError: If the category is not a string.
        """
        if not isinstance(value, MaterialEn):
            raise ValueError("Category must be a MaterialEnum")
        self._category = value

    @property
    def bbox(self) -> tuple[int, int, int, int]:
        """
        Get the bbox of the piece.

        Returns:
            tuple: four integers (x, y, w, h).
        """
        return self._bbox

    @bbox.setter
    def bbox(self, value: tuple[int, int, int, int]) -> None:
        """
        Set bounding box of the piece.

        Args:
            value (tuple): (x, y, w, h).

        Raises:
            ValueError: If the bbxox are not a tuple of int values.
        """
        if not (isinstance(value, tuple) and len(value) == 4 and all(isinstance(i, int) for i in value)):
            raise ValueError("Bounding box must be a tuple of four integers (x, y, w, h)")
        self._bbox = value

    @property
    def mean_colors(self) -> list[dict[str, tuple[int, int, int]]]:
        """
        Get the mean colors of the piece.

        Returns:
            list: A list of dictionaries with mean color and time.
        """
        return self._mean_colors

    @mean_colors.setter
    def mean_colors(self, value: list[dict[str, tuple[int, int, int]]]) -> None:
        """
        Set the mean colors of the piece.

        Args:
            value (list): A list of dictionaries with mean color and time.

        Raises:
            ValueError: If the mean colors are not a list of dictionaries with mean color and time.
        """
        if not (isinstance(value, list) and
                all(isinstance(i, dict) and 'mean_color' in i and 'time' in i for i in value)):
            raise ValueError("Mean colors must be a list of dictionaries with mean color and time")
        self._mean_colors = value

    @property
    def positions(self) -> list[dict[str, tuple[float, float]]]:
        """
        Get the positions of the piece.

        Returns:
            list: A list of dictionaries with position and time.
        """
        return self._positions

    @positions.setter
    def positions(self, value: list[dict[str, tuple[float, float]]]) -> None:
        """
        Set the positions of the piece.

        Args:
            value (list): A list of dictionaries with position and time.

        Raises:
            ValueError: If the positions are not a list of dictionaries with position and time.
        """
        if not (isinstance(value, list) and
                all(isinstance(i, dict) and 'position' in i and 'time' in i for i in value)):
            raise ValueError("Positions must be a list of dictionaries with position and time")
        self._positions = value

    @property
    def areas(self) -> list[dict[str, int]]:
        """
        Get the areas of the piece.

        Returns:
            list: A list of dictionaries with area and time.
        """
        return self._areas

    @areas.setter
    def areas(self, value: list[dict[str, int]]) -> None:
        """
        Set the area of the piece.

        Args:
            value (list): A list of dictionaries with area and time.

        Raises:
            ValueError: If the areas are not a list of dictionaries with position and time.
        """
        if not (isinstance(value, list) and
                all(isinstance(i, dict) and 'area' in i and 'time' in i for i in value)):
            raise ValueError("Areas must be a list of dictionaries with position and time")
        self._areas = value

    @property
    def speed(self):
        """
        Get the speed of the piece

        Returns:
            tuple: The speed of the piece as a tuple of two numbers (x, y).
        """
        return self._speed

    @speed.setter
    def speed(self, value: tuple) -> None:
        """
        Set the speed of the piece.

        Args:
            value (tuple): speed.

        Raises:
            ValueError: If the speed is not a tuple
        """
        if not (isinstance(value, tuple) and len(value) == 2 and all(isinstance(i, (int, float)) for i in value)):
            raise ValueError("Position must be a tuple of two numbers (int or float)")
        self._speed = value

    # ----- Representation functions

    def __repr__(self) -> str:
        """
        Return a string representation of the BasePiece instance.

        Returns:
            str: A string representation of the BasePiece instance.
        """
        return (f"BasePiece(name={self._name}, category={self._category}, bbox={self._bbox}, mean_colors="
                f"{self._mean_colors}, positions={self._positions}), areas={self._areas}, speed={self._speed})")

    def __str__(self):
        """
        Return a user-friendly string representation of the BasePiece instance.

        Returns:
            str: A user-friendly string representation of the BasePiece instance.
        """
        return (f"Piece: {self._name}, Category: {self._category}, bbox: {self._bbox}, Mean Colors: "
                f"{self._mean_colors}, Positions: {self._positions}, Areas: {self._areas}, Speed: {self._speed}")

    # ----- Bounding box functions

    def get_bbox_points(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Get the bounding box points.

        Returns:
            tuple[int, int]: point1.
            tuple[int, int]: point2.
        """
        point1 = (self._bbox[0], self._bbox[1])
        point2 = (int(self._bbox[0]+self._bbox[2]), int(self._bbox[1]+self._bbox[3]))
        return point1, point2

    # ----- Mean color functions

    def add_mean_color(self, mean_color: tuple[int, int, int]) -> None:
        """
        Add a new mean color with the current time.

        Args:
            mean_color (tuple): The mean color of the piece as a tuple of three integers (B, G, R).
        """
        if not (isinstance(mean_color, tuple) and len(mean_color) == 3 and all(isinstance(i, int) for i in mean_color)):
            raise ValueError("Mean color must be a tuple of three integers")
        self._mean_colors.append({'mean_color': mean_color, 'time': time.time()})

    def calculate_mean_color(self) -> tuple[int, int, int]:
        """
        Calculate the overall mean color using all mean colors.

        Returns:
            tuple: The overall mean color as a tuple of three integers (B, G, R).

        Raises:
            ValueError: If there are no mean colors available.
        """
        if self._mean_colors == []:
            raise ValueError("No mean colors available")

        total_b, total_g, total_r = 0, 0, 0
        for entry in self._mean_colors:
            b, g, r = entry['mean_color']
            total_b += b
            total_g += g
            total_r += r

        count = len(self._mean_colors)
        return (total_b // count, total_g // count, total_r // count)

    def calculate_mean_color_lab(self) -> tuple[int, int, int]:
        """
        Calculate the overall mean color in LAB color space using all mean colors.

        Returns:
            tuple: The overall mean color in LAB color space as a tuple of three integers (L, A, B).

        Raises:
            ValueError: If there are no mean colors available.
        """
        piece_mean_color_lab = bgr_to_lab(self.calculate_mean_color())
        return piece_mean_color_lab

    def calculate_category(self) -> MaterialEn:
        """
        Get the category of the piece.

        Returns:
            str: The category of the piece.
        """
        material, dist = LabClassifier.which_material(self.calculate_mean_color_lab(), verbose=False)
        self._category = material
        self._name = material.name.lower()

        return self._category
    
    # ----- Position functions

    def add_position(self, position: tuple[float, float]) -> None:
        """
        Add a new position with the current time.

        Args:
            position (tuple): The position of the piece as a tuple of two numbers (x, y).

        Raises:
            ValueError: If the position is not a tuple of two numbers (int or float).
        """
        if not (isinstance(position, tuple) and len(position) == 2 and
                all(isinstance(i, (int, float)) for i in position)):
            raise ValueError("Position must be a tuple of two numbers (int or float)")
        self._positions.append({'position': position, 'time': time.time()})

    def get_last_positon(self) -> tuple[float, float]:
        """
        Get the last position of the piece.

        Returns:
            tuple: The last position of the piece as a tuple of two numbers (x, y).

        Raises:
            ValueError: If there are no positions available.
        """
        if len(self.positions) == 0:
            raise ValueError("No positions available")
        return self.positions[-1]['position']

    # ----- Area functions

    def add_area(self, area: int) -> None:
        """
        Add a new area with the current time.

        Args:
            area (int): The area of the piece in pixels.

        Raises:
            ValueError: If the area is not an integer.
        """
        if not isinstance(area, int):
            raise ValueError("Area must be an integer")
        self._areas.append({'area': area, 'time': time.time()})

    def calculate_area(self) -> int:
        """
        Calculate the overall area using all areas.

        Returns:
            int: The overall area in pixels.

        Raises:
            ValueError: If there are no areas available.
        """
        if self._areas == []:
            raise ValueError("No areas available")

        total_area = 0
        for entry in self._areas:
            total_area += entry['area']

        count = len(self._areas)
        return total_area // count  # redondea el resultado hacia abajo al mas cercano

    # ----- Speed functions

    def calculate_speed(self) -> tuple[float, float]:
        """
        Calculate the speed of the piece using the positions and times.

        Returns:
            tuple: The speed of the piece as a tuple of two numbers (vx, vy).

        Raises:
            ValueError: If there are not enough positions available to calculate the speed.
            ValueError: If the time difference is zero.
        """
        if len(self._positions) < 2:
            raise ValueError("At least two positions are required to calculate the speed")

        # Calculate the differences in position and time
        delta_x = self._positions[-1]['position'][0] - self._positions[0]['position'][0]
        delta_y = self._positions[-1]['position'][1] - self._positions[0]['position'][1]
        delta_time = self._positions[-1]['time'] - self._positions[0]['time']

        if delta_time == 0:
            raise ValueError("The time difference must be greater than zero")

        # Calculate the speed
        vx = delta_x / delta_time
        vy = delta_y / delta_time

        self._speed = (vx, vy)

        return self._speed

    # ----- Other methods

    def update(self, piece: Piece | None = None) -> None:
        """
        Update with other piece.

        Args:
            piece (Piece): The piece to update with.
        """
        if piece is not None:
            if piece.bbox:
                self.bbox = piece.bbox
            self._mean_colors.append(piece.mean_colors[-1])
            self._positions.append(piece.positions[-1])
            if len(piece.areas) > 0:
                self._areas.append(piece.areas[-1])
        # Calculate
        if len(self._positions) > 1:
            _ = self.calculate_speed()
        if len(self._mean_colors) > 0:
            _ = self.calculate_category()

    def draw(self, image: np.ndarray, track: bool = False) -> None:
        """
        Draw the piece information on the image.

        Args:
            image (np.ndarray): The image to draw on.
            track (bool). Draw or not the track
        """
        color = self.mean_colors[0]['mean_color']
        thickness = 1

        if track:
            # Draw the trajectory
            for i in range(1, len(self._positions)):
                start_point = (int(self._positions[i-1]['position'][0]), int(self._positions[i-1]['position'][1]))
                end_point = (int(self._positions[i]['position'][0]), int(self._positions[i]['position'][1]))
                cv2.line(image, start_point, end_point, color, thickness)

        # Draw the current position
        if self._positions:
            current_position = (int(self._positions[-1]['position'][0]), int(self._positions[-1]['position'][1]))
            cv2.circle(image, current_position, 5, (0, 0, 0), -1)

        # Draw bounding box
        if self._bbox:
            point1, point2 = self.get_bbox_points()
            # Dibujar el rectángulo en la imagen
            cv2.rectangle(img=image, pt1=point1, pt2=point2, color=color, thickness=thickness)

        # Draw the name
        thickness = 2
        if self._bbox and self._name:
            cv2.putText(image, f"{self._name}({self.id})", (self.bbox[0] - 10, self.bbox[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, thickness)

    def pack(self) -> bytes:
        """
        Pack the piece information into a dictionary.

        Returns:
            dict: A dictionary with the piece information.
        """
        area = self.calculate_area()
        position = self.get_last_positon()
        speed = self.calculate_speed()
        mean_color = self.calculate_mean_color()
        category = self.calculate_category()

        piece_dict = {'id': self._id,
                      'name': self._name,
                      'category': category.value,
                      'bbox': self._bbox,
                      'mean_color': mean_color,
                      'position': position,
                      'area': area,
                      'speed': speed,
                      'timestamp': self.positions[-1]['time']
                      }

        return json.dumps(piece_dict).encode("utf-8")
