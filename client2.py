import os
import socket
import threading
from dotenv import load_dotenv

load_dotenv()


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(f"{message}")
        except socket.error:
            print("There was an error, connection lost.")
            break


host = os.getenv("IP")
port = 8765

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

client_name = input("Enter your name: ")
client_socket.send(client_name.encode("utf-8"))

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

while True:
    message = input("")
    client_socket.send(message.encode("utf-8"))
