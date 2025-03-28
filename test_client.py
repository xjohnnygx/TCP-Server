import time
import pytest
from socket import socket, AF_INET, SOCK_STREAM

def test_client_feedback_in_uppercase():
    client=socket(AF_INET, SOCK_STREAM)
    client.connect(("localhost", 5000))
    message = client.recv(1024).decode()
    assert message == "ENTER USERNAME"

def test_client_disconnect():
    client=socket(AF_INET, SOCK_STREAM)
    client.connect(("localhost", 5000))
    message = client.recv(1024).decode()
    assert message == "ENTER USERNAME"
    client.sendall(b"SOMENAME")
    message = client.recv(1024).decode()
    assert message == "Connection Established, type 'DESCONEXION' to close the connection."
    time.sleep(2)
    try:
        client.sendall(b"DESCONEXION") # raise Exception
    except:
        assert True