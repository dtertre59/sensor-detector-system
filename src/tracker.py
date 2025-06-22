"""
tracker.py
"""

import numpy as np
import cv2
from collections import defaultdict
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

    def __init__(self, x_min: float = 0, x_max: float = 640, y_max: float = 580,
                 min_area: int = 300, tolerance: float = 0.1):
        """
        Initialize the Tracker instance. TODO
        """
        self._pieces: list[Piece] = []
        self._pieces_all_info: list[tuple[Piece, int]] = []

        self._counter = 0
        self._x_min = x_min
        self._x_max = x_max
        self._y_max = y_max

        # Minimum area of a piece to be tracked
        self._min_area = min_area

        # limits
        self._x_addition_limit = x_min + 100
        self._x_expulsion_limit = x_max - 100

        # Tolerance for y position
        self._tolerance = tolerance

    def get_short_description(self, pieces: list[Piece] | None = None) -> str:
        """
        Get a short description of the Tracker instance.
        """
        if pieces is None:
            pieces = self._pieces
        text = ''
        for piece in pieces:
            text += f' {piece.name}({piece.id}) |'
        return text[1:-2]

    def add_piece(self, piece: Piece, verbose: bool = False) -> None:
        """
        Add a piece to the tracker.
        """
        if piece in self._pieces:
            raise Exception('Piece is already in the list')

        piece.id = self._counter
        piece.update()
        self._pieces.append(piece)
        self._pieces_all_info.append((piece, 0))
        if verbose:
            print(f'ADD {piece.name}({piece.id})')
        self._counter += 1

    def one_strike(self, piece: Piece, max_strikes: int = 3, verbose: bool = False) -> None:
        """
        Put one strike to a piece
        """
        strike = None

        if piece not in self._pieces:
            raise Exception('Piece is not in the list')

        for index, data in enumerate(self._pieces_all_info):
            if data[0] == piece:
                self._pieces_all_info[index] = (self._pieces_all_info[index][0], (self._pieces_all_info[index][1] + 1))
                strike = self._pieces_all_info[index][1]
                if verbose:
                    print(f'ERR {piece.name}({piece.id}) -> number of strikes:', self._pieces_all_info[index][1])
                break
        else:
            raise Exception('Piece is not in the list of pieces with strikes')
        if strike > max_strikes:
            self.delete_piece(piece, verbose=verbose)

    def delete_piece(self, piece: Piece, verbose: bool = False):
        """
        Delete piece
        """
        self._pieces = [p for p in self._pieces if p != piece]
        self._pieces_all_info = [p for p in self._pieces_all_info if p[0] != piece]
        if verbose:
            print(f'DELETE {piece.name}({piece.id})')

    def delete_pieces(self, pieces: list[Piece]):
        """ delete pieces """
        self._pieces = [p for p in self._pieces if p not in pieces]
        self._pieces_all_info = [p for p in self._pieces_all_info if p[0] not in pieces]

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

    def discard_filters(self, piece: Piece, verbose: bool = False) -> bool:
        """
        Discard piece if it does not pass the filters.

        Args:
            piece (Piece): The piece to check.
            verbose (bool): Whether to print information.

        Returns:
            bool: True if the piece passes the filters, False otherwise.
        """
        # Filter 1. size
        if piece.calculate_area() < self._min_area:
            if verbose:
                print(f'DISCARD {piece.name}({piece.id}): Is too small')
            return False

        # Filter 2. position limit 1
        if (piece.get_last_positon()[0] >= self._x_expulsion_limit):
            if verbose:
                print(f'DISCARD {piece.name}({piece.id}): Is out of range')
            return False

        # Filter 3. position limit 2
        if piece.get_last_positon()[0] > self._x_addition_limit:
            print(f'DISCARD {piece.name}({piece.id}): Is out of addition range:', piece.get_last_positon())
            #  TODO: Check if the piece is a division of another piece.
            # One piece in a frame are two or more pieces in the next frame.
            return False

        return True

    def update(self, new_pieces: list[Piece], verbose: bool = False) -> list[Piece]:
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
            print('')
            print('----- Tracker Update -----')
            print()
            print('Tracker Pieces before updating:', self.get_short_description())
            print('Number of pieces in image:', len(new_pieces))

        # Order new pieces by X poosition. Descending
        new_pieces.sort(key=lambda x: x.get_last_positon()[0], reverse=True)

        # new_pieces = [new_piece for new_piece in new_pieces if new_piece.calculate_area() > 2000]

        # # When the list is empty
        # if len(self._pieces) == 0:
        #     possible_pieces = [new_piece for new_piece in unmatched_new_pieces if
        #                        new_piece.get_last_positon()[0] < self._x_expulsion_limit]

        #     for new_piece in possible_pieces:
        #         self.add_piece(new_piece, verbose=verbose)
        #     return

        # ----- MATCHING PIECES ----- #

        if len(self._pieces) != 0:
            if verbose:
                print()

            matching_pieces: list[tuple[Piece, Piece, float]] = []

            for piece in self._pieces:
                new_pieces.sort(key=lambda x, piece=piece: self._calculate_similarity(piece, x), reverse=True)
                best_piece = new_pieces[0]
                best_similarity = self._calculate_similarity(piece, best_piece)
                # if verbose:
                #     print(f'{piece.name} -> Best match with piece {best_piece.id}:', best_piece.get_last_positon(),
                #           best_similarity, '%')
                matching_pieces.append((piece, best_piece, best_similarity))

            matching_pieces.sort(key=lambda x: x[2], reverse=True)

            # # Dict pieces with same new_piece
            # matching_pieces_dict = defaultdict(list)
            # for piece, best_piece, best_similarity in matching_pieces:
            #     matching_pieces_dict[best_piece.id].append(piece.name)
            # if verbose:
            #     print(matching_pieces_dict)

            # Strike or Merge those pieces

            for piece, best_piece, best_similarity in matching_pieces:
                try:
                    unmatched_new_pieces.remove(best_piece)
                except ValueError:
                    self.one_strike(piece, max_strikes=3, verbose=verbose)  # if strike > 3 del piece
                else:
                    piece.update(best_piece)
                    if verbose:
                        print(f'UPDATE {piece.name}({piece.id}) -> Best match with piece {best_piece.id}:', 
                              best_piece.get_last_positon(), round(best_similarity, 5), '%')

            # if verbose:
            #     print()
            #     print('My pieces after Match:', self.get_short_description())

        # ----- ADDING NEW PIECES ----- #

        if verbose:
            print()
            print('Number of unmatched pieces:', len(unmatched_new_pieces))

        if len(unmatched_new_pieces) != 0:
            if verbose:
                print()
            for new_piece in unmatched_new_pieces:
                if not self.discard_filters(new_piece, verbose=verbose):
                    continue
                # Add new piece
                self.add_piece(new_piece, verbose=verbose)

        # Return the pieces that are out of range
        out_of_range_pieces = [piece for piece in self._pieces if
                               piece.get_last_positon()[0] >= self._x_expulsion_limit]
        # Update the list of pieces
        self.delete_pieces(out_of_range_pieces)

        if verbose:
            print()
            print('My pieces after updating:', self.get_short_description())
            print('Released pieces:', self.get_short_description(out_of_range_pieces))
            print()
            print('--------------------------')
            print()
        return out_of_range_pieces

    def draw(self, frame: np.ndarray, track: bool = False) -> None:
        """
        Draw the tracks of the pieces on the image.

        Args:
            frame: The image to draw the tracks on.
        """
        # Green line. Addition limit
        start_point = (self._x_addition_limit, 0)
        end_point = (self._x_addition_limit, frame.shape[0])
        cv2.line(frame, start_point, end_point, (0, 255, 0), 2)
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
