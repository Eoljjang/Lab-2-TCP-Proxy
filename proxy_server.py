
import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

# Send some data(request) to host:port
# This is where the proxy sends request from main client to target server.
def send_request(host, port, request):
    # Create a new socket in "with" block (ensure connection closure)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket: #
        client_socket.connect((host,port)) # connect socket to host:port
        client_socket.send(request) # Send request
        client_socket.shutdown(socket.SHUT_WR) # shut socket to further writes. Tells server we're done sending.

        # Assemble response. Remember that recv(bytes) blocks until it receives data!
        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while len(data) > 0: # Keep reading until connection terminates
            data = client_socket.recv(BYTES_TO_READ)
            result += data
        # return response
        return result
    
# Handle incoming connection that has been accepted by server.
# This is the part where the proxy acts as a client to the target server.
def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        request = b''
        while True: # While client is keeping the socket open.
            data = conn.recv(BYTES_TO_READ) # Read data from socket.
            if not data: #If the socket has been closed to further writes, break.
                break
            print(data)
            request += data
        response = send_request("www.google.com", 80, request) # And send it as a request to www.google.com
        conn.sendall(response) # Return the response from www.google.com BACK to the main client.

# This is where the proxy acts as a server to the main client.
def start_server():
    # Create socket in "with" block to ensure it gets auto-closed when done
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the server to a specific host & port on this machine.
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))

        # Allow you to reuse this socket address during linger, and some other benefits.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Allow queueing of up to 2 connections.
        server_socket.listen(2) 

        # Wait for incomming connection. Once one arrives, accept it and create a new socket "conn" to interact with.
        conn, addr = server_socket.accept()

        # Pass 'conn' off to handle_connection to do some logic
        handle_connection(conn, addr)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(PROXY_SERVER_HOST, PROXY_SERVER_PORT)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2) # Allow queueing of up to 2 connections.

        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target=handle_connection, args=(conn,addr))
            thread.run()

start_server()
#start_threaded_server()

'''
See which ports are active:
lsof -nP | grep LISTEN

Kill processes (in increasing order of danger):
pkill python
sudo kill <pid>
sudo kill -9 <pid>
'''