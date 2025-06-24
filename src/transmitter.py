"""
piece_transmitter.py
"""

import socket
import struct

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

    def initialize(self, multicast: bool = False) -> None:
        """
        Initialize the transmitter
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send_piece(self, message: bytes) -> None:
        """
        Send a message to the peers.

        Args:
            message (bytes): The piece to send.
        """

        try:
            self.sock.sendall(message)
            print(f"Sent: {message}")

            # Optionally, receive a response
            response = self.sock.recv(1024).decode("utf-8")
            print(f"Received: {response}")

        except ConnectionError as e:
            print(f"Connection error: {e}")


class MulticastTransmitter():
    """
    This class is responsible for transmitting the pieces to the peers using multicast.
    """
    def __init__(self, mc_host: str, mc_port: int, mc_iface: str = '127.0.0.1'):
        self.mc_host = mc_host  # dirección de multicast.
        self.mc_port = mc_port
        self.mc_iface = mc_iface    # 'localhost' Interfaz de Red 

        self.sock = None

    def initialize(self):
        """
        Initialize the transmitter
        """
        # Crear el socket UDP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # Permitir el reenvío de paquetes multicast
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)  # Time-to-live (TTL) 255 para la propagación

        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(self.mc_iface)) # Si pongo 0.0.0.0 no va, con 127.0.0.1 si

    def send_multicast(self, message: bytes) -> None:
        """
        Send a message to the peers.

        Args:
            message (bytes)
        """
        self.sock.sendto(message, (self.mc_host, self.mc_port))


class RawPiece():
    def __init__(self, material: int, timestamp_ms: int, speed: float):
        self.material = material
        self.timestamp_ms = timestamp_ms
        self.speed = speed

    def pack(self) -> bytes:
        return struct.pack('ILf', self.material, self.timestamp_ms, self.speed)




if __name__ == "__main__":
    # transmitter = Transmitter("localhost", 5001)
    # transmitter.initialize()
    mctransmiter = MulticastTransmitter("224.0.0.1", 5007, "127.0.0.1")
    mctransmiter.initialize()
    # mctransmiter.send_multicast(b"Hello, World!")

    # transmitter.send_piece('a')
    # transmitter.send_piece('b')
    # transmitter.send_piece('c')
    # transmitter.send_piece('d')
    piece_0 = Piece(id=0, 
                    name='unknown', 
                    category='unknown',
                    bbox=(0, 0, 0, 0)
                    )
    piece_0.add_position((0, 0))
    piece_0.add_position((0, 1))
    piece_0.add_position((0, 2))

    piece_0.add_mean_color((0, 0, 0))
    piece_0.add_mean_color((0, 1, 0))
    piece_0.add_mean_color((0, 0, 1))

    piece_0.add_area(100)
    piece_0.add_area(100)
    piece_0.add_area(100)

    piece_0.calculate_speed()

    piece_raw = piece_0.pack()

    # print(piece_raw)
    # mctransmiter.send_multicast(piece_raw)
    import time
    now_timestamp = time.time()
    now_timestamp_ms = int(now_timestamp * 1000)  # Convert to milliseconds
    print(now_timestamp_ms)
    rp = RawPiece(2, (now_timestamp_ms - 1), 10.0).pack()
    print(rp)
    mctransmiter.send_multicast(rp)
