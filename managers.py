from socket import socket

class ConnectionManager:
    def __init__(self):
        self.activeConnections: list[socket] = []

    def connect(self, client: socket):
        self.activeConnections.append(client)

    def disconnect(self, client: socket):
        self.activeConnections.remove(client)

    def broadcast(self, client: socket, message: str):
        if client in self.activeConnections:
            for connection in self.activeConnections:
                if connection != client:
                    connection.sendall( message.upper().encode() )

    def serve(self, client: socket, username: str):
        while True:
            try:
                message = client.recv(1024).decode()
                if message == "DESCONEXION":
                    print(message)
                    self.broadcast(client, f"{username} left.")
                    self.disconnect(client)
                    client.close()
                    break
                print(message)
                self.broadcast(client, message)
            except:
                self.broadcast(client, f"{username} left.")
                self.disconnect(client)
                client.close()
                break