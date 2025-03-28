import pytest
import socket
import threading
import time
from managers import ConnectionManager
from server import HOST, PORT

# Helper function to create a client
def create_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    return client

@pytest.fixture
def start_server():
    """Starts the TCP server in a separate thread before running tests."""
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Allow time for server to start
    return server_thread

def run_server():
    """Runs the actual server logic."""
    manager = ConnectionManager()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    while True:
        client, address = server.accept()
        manager.connect(client)
        client.sendall(b"enter username")
        username = client.recv(1024).decode()
        manager.broadcast(client, f"{username} joined.")
        client.sendall(b"Connection Established, type 'DESCONEXION' to close the connection.")
        task = threading.Thread(target=manager.serve, args=(client, username))
        task.start()

# ✅ Test 1: Sending a normal message should be received in uppercase
def test_message_broadcast(start_server):
    client1 = create_client()
    client2 = create_client()

    # Receive initial server prompts
    client1.recv(1024)
    client1.sendall(b"User1")
    client2.recv(1024)
    client2.sendall(b"User2")

    client1.recv(1024)  # "Connection Established"
    client2.recv(1024)

    # Send a message from client1
    client1.sendall(b"hello world")
    time.sleep(0.5)  # Allow time for message to be processed

    # Client2 should receive it in UPPERCASE
    response = client2.recv(1024).decode()
    assert response == "HELLO WORLD"

    client1.close()
    client2.close()

# ✅ Test 2: Client should disconnect properly
def test_client_disconnect(start_server):
    client = create_client()

    # Receive initial prompts
    client.recv(1024)
    client.sendall(b"UserTest")
    client.recv(1024)

    # Send "DESCONEXION"
    client.sendall(b"DESCONEXION")
    time.sleep(0.5)  # Allow time for disconnect

    # Try sending another message (should fail)
    with pytest.raises(OSError):  # Connection should be closed
        client.sendall(b"Still here?")

    client.close()
