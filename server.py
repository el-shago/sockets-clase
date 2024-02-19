import os
import socket
import threading
from dotenv import load_dotenv

load_dotenv()

def handle_client(client_socket, client_address, client_name):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')

            if message.lower() == "adios":
                break

            formatted_message = f"{client_name}: {message}"

            for other_client_socket, _, _ in clients:
                if other_client_socket != client_socket:
                    try:
                        other_client_socket.send(formatted_message.encode("utf-8"))
                    except socket.error:
                        pass
    finally:
        client_socket.close()
        clients.remove((client_socket, client_address, client_name))


host = os.getenv("IP")
port = 8765

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Server listening on {host}:{port}")

clients = []

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection accepted from {client_address}")

    client_socket.send("Enter your name: ".encode("utf-8"))
    client_name = client_socket.recv(1024).decode("utf-8")

    clients.append((client_socket, client_address, client_name))

    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, client_name))
    client_handler.start()