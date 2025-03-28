from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM

PORT=5000
HOST="localhost"

username=input("ENTER USERNAME: ").upper()
connection=socket(AF_INET, SOCK_STREAM)
connection.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = connection.recv(1024).decode()
            if message == "ENTER USERNAME":
                connection.sendall(username.encode())
            else:
                print(message)
        except:
            print("\nconnection closed.")
            connection.close()
            break

def send():
    while True:
        message = input("> ")
        if message == "DESCONEXION":
            connection.sendall(b"DESCONEXION")
            connection.close()
            break
        connection.sendall(f"({username}) {message}".encode())


receiveThread=Thread(target=receive)
receiveThread.start()

sendThread=Thread(target=send)
sendThread.start()

receiveThread.join()
sendThread.join()