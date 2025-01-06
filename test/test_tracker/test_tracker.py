"""
test_tracker.py
"""
import cv2

from src.utils import show_image
from src.tracker import Tracker
from src.piece.piece import Piece


def test_instances():
    """
    test
    """
    tracker = Tracker()
    print(tracker)


def test_update():
    """
    test
    """
    tracker = Tracker(tolerance=0.01)

    piece = Piece('pieza_prueba', 'metal')
    mean_color = (255, 0, 255)
    piece.add_mean_color(mean_color)
    pos_1 = (0, 0)
    piece.add_position(pos_1)

    tracker.update([piece])
    print(tracker)

    piece = Piece('pieza_prueba', 'metal')
    mean_color = (255, 10, 255)
    piece.add_mean_color(mean_color)
    pos_1 = (30, 7)
    piece.add_position(pos_1)

    tracker.update([piece])
    print(tracker)

    piece = Piece('pieza_prueba', 'metal')
    mean_color = (255, 111, 255)
    piece.add_mean_color(mean_color)
    pos_1 = (40, 10)
    piece.add_position(pos_1)

    tracker.update([piece])
    print(tracker)

    piece = Piece('pieza_prueba', 'metal')
    mean_color = (244, 111, 244)
    piece.add_mean_color(mean_color)
    pos_1 = (110, 4)
    piece.add_position(pos_1)

    tracker.update([piece])
    print(tracker)

    piece = Piece('pieza_prueba', 'metal')
    mean_color = (222, 111, 222)
    piece.add_mean_color(mean_color)
    pos_1 = (1, 4)
    piece.add_position(pos_1)

    tracker.update([piece])
    print(tracker)

    piece = Piece('pieza_prueba', 'metal')
    mean_color = (111, 111, 222)
    piece.add_mean_color(mean_color)
    pos_1 = (19, 5)
    piece.add_position(pos_1)

    tracker.update([piece])
    print(tracker)


    piece = Piece('pieza_prueba', 'metal')
    mean_color = (111, 111, 111)
    piece.add_mean_color(mean_color)
    pos_1 = (800, 4)
    piece.add_position(pos_1)

    # PIECE OUT OF RANGE POP OF THE LIST AND GOES TO RESULT
    result = tracker.update([piece])
    print(tracker)
    print(result)


def test_draw():
    """
    test
    """
    image = cv2.imread('data/images/samples/laton_1.jpeg')
    image = cv2.resize(image, (640, 640))
    show_image(image)

    tracker = Tracker(x_min=10, x_max=630, y_max=640, tolerance=0.1)

    # Add piece
    piece = Piece('pieza_prueba', 'metal', bbox=(20,20,20,20))
    mean_color = (0, 111, 244)
    piece.add_mean_color(mean_color)
    pos_1 = (110, 110)
    piece.add_position(pos_1)

    tracker.update([piece])

    tracker.draw(image)
    show_image(image)

    # Add piece
    piece = Piece('pieza_prueba', 'metal')
    mean_color = (244, 111, 244)
    piece.add_mean_color(mean_color)
    pos_1 = (220, 115)
    piece.add_position(pos_1)

    tracker.update([piece])

    # tracker.draw(image)
    show_image(image)

    # Add piece
    piece = Piece('pieza_prueba', 'metal', bbox=(500,20,20,20))
    mean_color = (0, 111, 244)
    piece.add_mean_color(mean_color)
    pos_1 = (550, 105)
    piece.add_position(pos_1)

    tracker.update([piece])

    tracker.draw(image)
    show_image(image)


def main():
    """
    main
    """
    test_instances()
    test_update()
    test_draw()


if __name__ == '__main__':
    main()
