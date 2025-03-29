
import time
import socket


# Crear un socket de tipo TCP/IP

# HOST = "localhost"  # Escucha en todas las interfaces de red
# PORT = 5001        # Puerto donde escuchará

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
#     server_sock.bind((HOST, PORT))
#     server_sock.listen()
#     print(f"Listening on {HOST}:{PORT}")

#     conn, addr = server_sock.accept()
#     with conn:
#         print(f"Connected by {addr}")
#         while True:
#             data = conn.recv(1024)  # Recibe hasta 1024 bytes
#             if not data:
#                 break  # Sale si no hay más datos
#             print(f"Received: {data.decode('utf-8')}")

#             message = b"ACK"
#             message = b'{"id": 0, "name": "unknown", "category": "unknown", "bbox": [0, 0, 0, 0], "mean_color": [0, 0, 0], "position": [0, 2], "area": 100, "speed": [0.0, 932067.5555555555], "timestamp": 1743187168.623563}'
#             conn.sendall(message)  # Responde con una confirmación opcional

# --------------------------------------------------------------- #
# MULTICAST UDP
# --------------------------------------------------------------- #

# import socket
# import struct

# MCAST_GRP = '224.0.0.1'  # Dirección multicast
# MCAST_PORT = 5007        # Puerto de escucha

# # Crear el socket UDP
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# # Permitir la recepción de datos en el grupo multicast
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# # Asociar el socket a la dirección multicast y puerto
# sock.bind(('', MCAST_PORT))

# # Unirse al grupo multicast en la interfaz lo0 (loopback)
# mreq = struct.pack('4s4s', socket.inet_aton(MCAST_GRP), socket.inet_aton('127.0.0.1'))
# sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# print(f"Esperando mensajes en {MCAST_GRP}:{MCAST_PORT}...")

# while True:
#     data, addr = sock.recvfrom(1024)  # Recibir datos
#     print(f"Recibido mensaje de {addr}: {data.decode()}")


import socket
import struct
import time

# Configuración
MCAST_GRP = '224.0.0.1'  # Dirección de grupo multicast
MCAST_PORT = 5007  # Puerto de multicast

# Crear el socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Permitir el reenvío de paquetes multicast
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)  # Time-to-live (TTL) 255 para la propagación

sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton('127.0.0.1')) # Si pongo 0.0.0.0 no va

# Enviar mensaje al grupo multicast
message = b'Hola, este es un mensaje de servidor multicast!'

while True:
    # Enviar el mensaje al grupo multicast
    sock.sendto(message, (MCAST_GRP, MCAST_PORT))
    print(f"Mensaje enviado a {MCAST_GRP}:{MCAST_PORT}")
    time.sleep(2)  # Enviar un mensaje cada 2 segundos
