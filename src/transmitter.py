"""
piece_transmitter.py
"""

import socket

from src.piece.piece import Piece


class Transmitter():
    """
    This class is responsible for transmitting the pieces to the peers.
    """
    def __init__(self, host: str, port: int):
        """
        Constructor
        """
        self.host = host
        self.port = port

        self.sock = None

    def initialize(self) -> None:
        """
        Initialize the transmitter
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send_piece(self, piece: Piece) -> None:
        """
        Send a piece to the peers.

        Args:
            piece (Piece): The piece to send.
        """

        message = piece

        try:
            self.sock.sendall(message.encode("utf-8"))
            print(f"Sent: {message}")

            # Optionally, receive a response
            response = self.sock.recv(1024).decode("utf-8")
            print(f"Received: {response}")

        except ConnectionError as e:
            print(f"Connection error: {e}")


if __name__ == "__main__":
    transmitter = Transmitter("localhost", 5001)
    transmitter.send_piece('a')
    transmitter.send_piece('b')
    transmitter.send_piece('c')
    transmitter.send_piece('d')
