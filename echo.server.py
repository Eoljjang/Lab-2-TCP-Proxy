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

# 1) Define host, address & buffer size.
HOST = "127.0.0.1" # (IP addr) equivalent to "localhost" -> Means this is your own PC.
PORT = 8080
BUFFER_SIZE = 1024

def main():
    # 2) Start server.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        # (question 3)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # 2) Bind server to the IP & Port
        s.bind((HOST, PORT))
        # 3) Set to listening mode -> Continuously listen for client connections.
        s.listen(2)
        
        while True:
            # 4) Accept client connection -> RECEIVES "conn" and "addr"
            # - "conn" = Socket that refers to the client (like a client_ID)
            # - "addr" = Address of the client [IP,Port]
            conn, addr = s.accept()
            print("Connected by", addr)
            
            # 5) Recieve request from client. Wait a bit.
            full_data = conn.recv(BUFFER_SIZE)
            time.sleep(0.5)

            # 6) Sends a response back to client.
            conn.sendall(full_data)
            conn.close()

if __name__ == "__main__":
    main()


