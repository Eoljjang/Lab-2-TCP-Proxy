# Listens for incoming connections
# Echos any received data (sends back w/e is sent to the server).
# Server-side code -> Typically it wouldn't be on the same machine (so you'd "host" it through a virtual environment)

# Notes:
# - Start the server: "python3 echo.server.py"
# - Terminal will just sit there. It isn't frozen, just waiting for a connection.
# - Run the "client.py" to connect to the server.

#!/usr/bin/env python3
import socket
import time
from threading import Thread

# 1) Define host, address & buffer size.
HOST = "127.0.0.1" # (IP addr) equivalent to "localhost" -> Means this is your own PC.
PORT = 8080
BUFFER_SIZE = 1024
BYTES_TO_READ = 4096

def handle_connection(conn, addr):
    with conn:
        print(f"Connected by{addr}")
        while True:
            data = conn.recv(BYTES_TO_READ) # Wait for request, and when you get it, receive it.
            if not data: # If an empty byte string is received ==> b''
                break
            print(data)
            conn.sendall(data) # Send data back to main client.

def start_server():
    # 2) Start server -> "with" handles all the connection closing, cleanup, etc. Without it, you'd have to close() connection manually.
    # (it's a Python specific feature)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # 2.1) Bind server to the IP & Port
        s.bind((HOST, PORT))
    
        # Make the port reusable (question 3)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen() # for incoming connections.
        conn, addr = s.accept() # conn = socket referring to client, addr = address of client [IP, Port]
        handle_connection(conn, addr) # Send client a response.

# Start multithreaded echo server
def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))

        # setsockopt (set socket option) -> socket.SO_REUSEADDR = reuse address -> set to 1 (any other socket can bind to the client).
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.listen(2) # Allow backlog of up to 2 connections => queue [waiting conn1, waiting conn2]

        # Allow the server to fork, and create threads for different connections.
        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection, args=(conn, addr)) # Start a new thread per new connection.
            thread.run()

start_threaded_server()