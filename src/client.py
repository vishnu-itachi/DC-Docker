import socket
import pickle
import time
import sys


class Client:
    host = None
    port = None
    socket = None

    def __init__(self, host=None, port=None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if host is None and port is None:
            return

        self.host = host
        self.port = port

        # Create a socket connection.
        self.socket.connect((host, port))
        print(f"connected to {host}:{port}")

    def connect(self, host, port):
        self.host = host
        self.port = port

        while True:
            try:
                self.socket.connect((host, port))
                sys.stdout.flush()
                break
            except Exception as e:
                print(f"error connecting to {host}:{port}")
                sys.stdout.flush()
                time.sleep(1)
                continue
        print(f"connected to {host}:{port}")

    def send(self, obj):
        data_string = pickle.dumps(obj)
        self.socket.send(data_string)
        print(f"Send {obj}")

    def close(self):
        self.socket.close()
