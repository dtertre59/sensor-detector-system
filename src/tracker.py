"""
tracker.py
"""

import numpy as np
import cv2
# from cv2.typing import MatLike

from src.piece.piece import Piece
# import src.utils as ut


class Tracker:
    """
    Class Tracker to track pieces in an image.

    position = (x, y)

    ----------> x
    |
    |
    |
    |
    y

    """

    def __init__(self, x_min: float = 0, x_max: float = 640, y_max: float = 580, tolerance: float = 0.1):
        """
        Initialize the Tracker instance. TODO
        """
        self._pieces: list[Piece] = []
        self._counter = 0
        self._x_min = x_min
        self._x_max = x_max
        self._y_max = y_max
        self._x_expulsion_limit = x_max - 100
        self._tolerance = tolerance

    # def _is_in_range(self, piece: Piece) -> int:
        # """
        # is Piece in range?

        # Args:
        #     piece (Piece):

        # Returns:
        #     int. -1 low, 0 yes, 1 up
        # """
        # last_position = piece.positions[-1]['position']
        # if last_position[0] < self._x_min:
        #     return -1
        # elif last_position[0] > self._x_max:
        #     return 1
        # return 0

    # def _is_the_same(self, piece: Piece) -> int:
    #     """
    #     TODO
    #     """

    #     for index, exist_piece in enumerate(self._pieces):
    #         first_position = exist_piece.get_last_positon()
    #         y_tolerance = self._y_max * self._tolerance
    #         updated_position = piece.get_last_positon()

    #         # 1. is behind
    #         if updated_position[0] < first_position[0]:
    #             continue
    #         # is in y line (x, y)
    #         elif (updated_position[1] > first_position[1] - y_tolerance and
    #               updated_position[1] < first_position[1] + y_tolerance):
    #             return index
    #         elif (piece.get_bbox_points()[0][1] < first_position[1] - y_tolerance and
    #               piece.get_bbox_points()[1][1] > first_position[1] + y_tolerance):
    #             print('Second try')
    #             return index
    #         else:
    #             continue
    #     print(f'not because tolerance: pass postion{first_position} new position{updated_position}')
    #     return -1

    def _calculate_similarity(self, piece: Piece, new_piece: Piece) -> float:
        """
        TODO
        """
        # # Calculate the probability of the match
        # # 1. Calculate the distance between the last position of the piece and the new piece
        # distance = ut.get_distance(piece.get_last_positon(), new_piece.get_last_positon())

        # # 2. Calulate the difference between the areas
        # area_difference = abs(piece.calculate_area() - new_piece.calculate_area())

        # # 3. X position difference
        # x_difference = abs(piece.get_last_positon()[0] - new_piece.get_last_positon()[0])

        # # 2. Calculate the probability, based on similarity of three factors.
        # probability = (0.5 / distance) + (0.5 / area_difference) + (2 / x_difference)

        # Increments
        delta_x = abs(piece.get_last_positon()[0] - new_piece.get_last_positon()[0])
        delta_y = abs(piece.get_last_positon()[1] - new_piece.get_last_positon()[1])
        delta_area = abs(piece.calculate_area() - new_piece.calculate_area())

        # Normalized weights
        w_x = 0.3
        w_y = 0.5
        w_area = 0.2

        # Euclidean distance normalized ponderated

        d = ((w_x * (delta_x / self._x_max) ** 2) +
             (w_y * (delta_y / self._y_max) ** 2) +
             (w_area * (delta_area / (self._x_max * self._y_max)) ** 2)
             ) ** 0.5

        # print('d', d)

        # Similarity index
        s = 1 - (d / ((w_x + w_y + w_area) ** 0.5))

        return s

    # def update(self, pieces: list[Piece], verbose: bool = False) -> list[Piece]:
    #     """
    #     Add a new piece to track or update an existing piece.

    #     Args:
    #         pieces (list[Piece]): The pieces to add or update.
    #         verbose (bool): Whether to print information.

    #     Returns:
    #         list[Pieces]: a list of pieces that comes outside our range. prepare to notify and Analyce
    #     """

    #     # local variables
    #     release_pieces = []

    #     if verbose:
    #         print('Number of pieces in image:', len(pieces))

    #     # When the list is empty
    #     if len(self._pieces) == 0:
    #         for piece in pieces:
    #             piece.id = self._counter
    #             piece.name = f'unknown-{piece.id}'
    #             self._counter += 1
    #             self._pieces.append(piece)

    #         if verbose:
    #             print('My pieces:', [p.name for p in self._pieces])
    #         return

    #     # When the list is not empty
    #     for index, piece in enumerate(pieces):
    #         print(piece)
    #         # Only if they are up to range min
    #         range_value = self._is_in_range(piece)

    #         if verbose:
    #             print(f'Detection {index} Range value:', range_value)

    #         # Piece in traker range
    #         if range_value == 0:
    #             piece_index = self._is_the_same(piece)

    #             if verbose:
    #                 print(f'Detection {index} is the same as piece:', piece_index)

    #             if piece_index >= 0:  # pieza localizada
    #                 self._pieces[piece_index].update(piece)
    #             else:  # pieza sin localizar -> la añadimos a la lista para trakearla
    #                 piece.name = f'unknown-{self._counter}'
    #                 print(piece.name)
    #                 self._counter += 1
    #                 self._pieces.append(piece)

    #         # Piece over max range (uncertain piece)
    #         # Como saber si ya ha sido detectada en esta zona y enviada, o todavia no?
    #         elif range_value == 1:
    #             print('Piece out of range')
    #             piece_index = self._is_the_same(piece)

    #             # Is the same
    #             if index >= 0:
    #                 release_pieces.append(self._pieces[piece_index])
    #                 # Remove the piece from the list
    #                 self._pieces.pop(piece_index)

    #                 # Notify
    #                 if verbose:
    #                     print('PIECE POP')

    #             # Not the same. It is an old piece
    #             else:
    #                 print('No piece to remove')
    #     if verbose:
    #         print('My pieces:', [p.name for p in self._pieces])
    #         print()

    #     return release_pieces

    # def update_2(self, new_pieces: list[Piece], verbose: bool = False) -> list[Piece]:

    #     for index, new_piece in enumerate(new_pieces):
    #         if new_piece.positions[-1]['position'][1] > self._x_max:
    #             print(f'{index} NEW PIECE OUT OF RANGE')
    #             continue

    #         # Piece in traker range
    #         if self._pieces != []:
    #             piece_index = self._is_the_same(new_piece)
    #             if piece_index >= 0:  # pieza localizada
    #                 print(f'{index} PIEZA LOCALIZADA')
    #                 self._pieces[piece_index].update(new_piece)
    #             else:
    #                 print(f'{index} NUEVA PIEZA')
    #                 new_piece.name = f'unknown-{self._counter}'
    #                 self._counter += 1
    #                 self._pieces.append(new_piece)
    #         else:
    #             print(f'{index} NUEVA PIEZA')
    #             new_piece.name = f'unknown-{self._counter}'
    #             self._counter += 1
    #             self._pieces.append(new_piece)

    def update_3(self, new_pieces: list[Piece], verbose: bool = False) -> list[Piece]:
        """
        Add a new piece to track or update an existing piece.

        Args:
            pieces (list[Piece]): The pieces to add or update.
            verbose (bool): Whether to print information.

        Returns:
            list[Pieces]: a list of pieces that comes outside our range. prepare to notify and Analyce
        """

        # local variables
        unmatched_new_pieces: list[Piece] = new_pieces.copy()

        if verbose:
            print('Number of pieces in image:', len(new_pieces))

        # Order new pieces by X poosition. Descending
        new_pieces.sort(key=lambda x: x.get_last_positon()[0], reverse=True)

        # new_pieces = [new_piece for new_piece in new_pieces if new_piece.calculate_area() > 2000]

        # When the list is empty
        if len(self._pieces) == 0:
            possible_pieces = [new_piece for new_piece in new_pieces if
                               new_piece.get_last_positon()[0] < self._x_expulsion_limit]

            for new_piece in possible_pieces:
                new_piece.id = self._counter
                new_piece.name = f'unknown-{new_piece.id}'
                self._counter += 1
                self._pieces.append(new_piece)

            if verbose:
                print('My pieces:', [p.name for p in self._pieces])
            return

        # When the list is not empty
        for piece in self._pieces:
            if verbose:
                print()
                print('Piece:', piece.name)
                print('Last Position:', piece.get_last_positon(), ' | Area:', piece.calculate_area())

            # for index, new_piece in enumerate(new_pieces):
            #     print('New Piece position:', new_piece.get_last_positon())

            possible_pieces = [new_piece for new_piece in new_pieces if
                               new_piece.get_last_positon()[0] > piece.get_last_positon()[0]]

            # Make an intersection with unmatched pieces
            possible_pieces = [new_piece for new_piece in possible_pieces if new_piece in unmatched_new_pieces]

            if verbose:
                print('Number of Possible pieces:', len(possible_pieces))
                for posible_piece in possible_pieces:
                    print(f'  - Possible Piece position: {posible_piece.get_last_positon()}'
                          f' | Area: {posible_piece.calculate_area()}')

            # Not possible pieces
            if len(possible_pieces) == 0:
                if verbose:
                    print(f'No possible pieces to match with piece {piece.name}')
                # unmatched_pieces.remove(piece)
                continue

            # ----- MATCHING PIECE ----- #

            # Probability
            for index, possible_piece in enumerate(possible_pieces):

                similarity = self._calculate_similarity(piece, possible_piece)

                if verbose:
                    print(f'Similarity {index}:', similarity * 100, '%')

            possible_pieces.sort(key=lambda x, piece=piece: self._calculate_similarity(piece, x), reverse=True)

            if verbose:
                print('Most Probable Piece:', possible_pieces[0].get_last_positon())

            piece.update(possible_pieces[0])

            unmatched_new_pieces.remove(possible_pieces[0])

        # ----- END OF MATCHING PIECES ----- #

        if verbose:
            print('Number of unmatched pieces', len(unmatched_new_pieces))

        # ----- ADDING NEW PIECES ----- #

        if len(unmatched_new_pieces) != 0:

            for new_piece in unmatched_new_pieces:
                # Filter 1. position and size
                if (new_piece.get_last_positon()[0] >= self._x_expulsion_limit or
                        new_piece.calculate_area() < 2000):
                    continue

                # Filter 2. Initial position x limit and division for other piece
                if new_piece.get_last_positon()[0] > 100:
                    # TODO: Check if the piece is a division of another piece.
                    # One piece in a frame are two or more pieces in the next frame.
                    continue

                new_piece.id = self._counter
                new_piece.name = f'unknown-{new_piece.id}'
                self._counter += 1
                if verbose:
                    print('New Piece:', new_piece.name, new_piece.get_last_positon())
                    print('Counter:', self._counter)
                self._pieces.append(new_piece)

        # Return the pieces that are out of range
        out_of_range_pieces = [piece for piece in self._pieces if
                               piece.get_last_positon()[0] >= self._x_expulsion_limit]
        # Update the list of pieces
        self._pieces = [piece for piece in self._pieces if piece.get_last_positon()[0] < self._x_expulsion_limit]

        return out_of_range_pieces

    def draw(self, frame: np.ndarray, track: bool = False) -> None:
        """
        Draw the tracks of the pieces on the image.

        Args:
            frame: The image to draw the tracks on.
        """
        # Red line. Limit
        start_point = (self._x_expulsion_limit, 0)
        end_point = (self._x_expulsion_limit, frame.shape[0])
        cv2.line(frame, start_point, end_point, (0, 0, 255), 2)
        # Pieces
        for piece in self._pieces:
            piece.draw(frame, track=track)

    def __repr__(self) -> str:
        """
        Return a string representation of the Tracker instance.

        Returns:
            str: A string representation of the Tracker instance.
        """
        return (f"Tracker(pieces={self._pieces}, counter={self._counter}, x_min={self._x_min}, "
                f"x_max={self._x_max}, tolerance={self._tolerance})")
