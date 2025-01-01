"""
test_base_piece.py
"""

from src.piece.piece import Piece


def test_instances():
    """
    test
    """
    piece = Piece('pieza_prueba', 'metal')
    if 'pieza_prueba' == piece.name:
        print('OK')
    if 'metal' == piece.category:
        print('OK')
    print(piece)


def test_add_mean_color():
    """
    test
    """
    piece = Piece('pieza_prueba', 'metal')
    mean_color = (255, 0, 255)
    mean_color_2 = (0, 255, 0)
    piece.add_mean_color(mean_color)
    piece.add_mean_color(mean_color_2)
    print(piece)
    print(piece.calculate_mean_color())


def test_add_position():
    """
    test
    """
    piece = Piece('pieza_prueba', 'metal')
    pos_1 = (0, 0)
    pos_2 = (20, 20)

    piece.add_position(pos_1)
    piece.add_position(pos_2)
    print(piece)
    print(piece.calculate_speed())
    print(piece)


def main():
    """
    main
    """
    test_instances()
    test_add_mean_color()
    test_add_position()


if __name__ == '__main__':
    main()
