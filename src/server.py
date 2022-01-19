import socket
import pickle
import sys


class Server:
    host = None
    port = None
    socket = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

        # Create a socket connection.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.listen()

    def listen(self, max_clients=5):
        self.socket.listen(max_clients)

    def recieve(self, numbytes=4096):
        print("inside recieve")
        sys.stdout.flush()
        conn, addr = self.socket.accept()
        print("after recieve")
        sys.stdout.flush()
        data = conn.recv(numbytes)
        print("got data")
        sys.stdout.flush()
        conn.close()
        print("returning data")
        sys.stdout.flush()
        return pickle.loads(data), addr

    def close(self):
        self.socket.close()
