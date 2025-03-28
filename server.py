from threading import Thread
from managers import ConnectionManager
from socket import socket, AF_INET, SOCK_STREAM

PORT=5000
HOST="localhost"

manager=ConnectionManager()
server=socket(AF_INET, SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"TCP server listening on {HOST}:{PORT}")

while True:
    client, address = server.accept()
    print(f"{address} connected")
    manager.connect(client)
    client.sendall(b"ENTER USERNAME")
    username = client.recv(1024).decode()
    manager.broadcast(client, f"{username} joined.")
    client.sendall(b"Connection Established, type 'DESCONEXION' to close the connection.")
    task = Thread(target=manager.serve, args=(client, username))
    task.start()