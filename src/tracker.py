"""
tracker.py
"""

import cv2
from cv2.typing import MatLike

from src.piece.piece import Piece


class Tracker:
    """
    Class Tracker to track pieces in an image.
    """

    def __init__(self, x_min: float = 0, x_max: float = 450, y_max: float = 640, tolerance: float = 0.1):
        """
        Initialize the Tracker instance. TODO
        """
        self._pieces: list[Piece] = []
        self._counter = 0
        self._x_min = x_min
        self._x_max = x_max
        self._y_max = y_max
        self._tolerance = tolerance

    def _is_in_range(self, piece: Piece) -> int:
        """
        is Piece in range?

        Args:
            piece (Piece):

        Returns:
            int. -1 low, 0 yes, 1 up
        """
        last_position = piece.positions[-1]['position']
        if last_position[0] < self._x_min:
            return -1
        elif last_position[0] > self._x_max:
            return 1
        return 0

    def _is_the_same(self, piece: Piece) -> int:
        """
        TODO
        """
        for index, exist_piece in enumerate(self._pieces):
            first_position = exist_piece.get_last_positon()
            y_tolerance = self._y_max * self._tolerance
            updated_position = piece.get_last_positon()
            # 1. is behind
            if updated_position[0] < first_position[0]:
                continue
            # is in y line
            elif (updated_position[1] > first_position[1] - y_tolerance and
                  updated_position[1] < first_position[1] + y_tolerance):
                return index
            else:
                print(f'not becaulse tolerance: {first_position[1] + y_tolerance}')
                continue
        return -1

    def update(self, pieces: list[Piece]) -> list[Piece]:
        """
        Add a new piece to track or update an existing piece.

        Args:
            pieces (list[Piece]): The pieces to add or update.

        Returns:
            list[Pieces]: a list of pieces that comes outside our range. prepare to notify and Analyce
        """

        release_pieces = []

        # When the list is empty
        if len(pieces) == 0:
            for piece in pieces:
                piece.name = f'unknown-{self._counter}'
                self._counter += 1
                self._pieces.append(piece)
            return

        for piece in pieces:
            # Only if they are up to range min
            range_value = self._is_in_range(piece)
            if range_value >= 0:
                piece_index = self._is_the_same(piece)
                print('Is the same', piece_index)
                if piece_index >= 0:  # pieza localizada
                    self._pieces[piece_index].update(piece)
                else:  # pieza sin localizar -> la añadimos a la lista para trakearla
                    piece.name = f'unknown-{self._counter}'
                    self._counter += 1
                    self._pieces.append(piece)

                if range_value == 1:  # Only if they are up to max
                    # save piece
                    release_pieces.append(self._pieces[piece_index])
                    # Remove the piece from the list
                    self._pieces.pop(piece_index)
                    # Notify
                    print('PIECE POP')
        return release_pieces

    def draw(self, image: MatLike) -> None:
        """
        Draw the tracks of the pieces on the image.

        Args:
            image (MatLike): The image to draw the tracks on.
        """
        # TODO
        # Red line. Limit
        start_point = (self._x_max, 0)
        end_point = (self._x_max, image.shape[0])
        cv2.line(image, start_point, end_point, (0, 0, 255), 2)
        for piece in self._pieces:
            piece.draw(image, track=False)

    def __repr__(self) -> str:
        """
        Return a string representation of the Tracker instance.

        Returns:
            str: A string representation of the Tracker instance.
        """
        return (f"Tracker(pieces={self._pieces}, counter={self._counter}, x_min={self._x_min}, "
                f"x_max={self._x_max}, tolerance={self._tolerance})")
