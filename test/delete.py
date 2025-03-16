import socket

HOST = "localhost"  # Escucha en todas las interfaces de red
PORT = 5001        # Puerto donde escuchará

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    print(f"Listening on {HOST}:{PORT}...")

    conn, addr = server_sock.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)  # Recibe hasta 1024 bytes
            if not data:
                break  # Sale si no hay más datos
            print(f"Received: {data.decode('utf-8')}")
            conn.sendall(b"ACK")  # Responde con una confirmación opcional
