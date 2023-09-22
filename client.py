# Client-side code
# Connects to, and requests info from server

import socket

BYTES_TO_READ = 4096 # How much data you're willing to accept.

def get(host, port):
  request = b"GET / HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n"
  # 1) Intialize socket
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
  # AF_INET = IPV4
  # AP_INET6 = IPV6
  # socket.SOCK_STREAM = TCP 
  # socket.SOCK_DGRAM = UDP

  # 2) Connect to server & make request
  s.connect((host,port)) 
  s.send(request)

  # 3) State that "you're done sending requests" \\ Shut down the 'write' side, now ready to receive.
  s.shutdown(socket.SHUT_WR) 

  # 4) Continuously receiving the response from server.# Keep reading incoming data (from server)
  result = s.recv(BYTES_TO_READ)
  while(len(result) > 0): # Keep reading the response until the sent response is empty.
    print(result) # Outputs to terminal.
    result = s.recv(BYTES_TO_READ)

  # 5) Close the socket.
  s.close()

#get("www.google.com", 80) # GET function that makes a request to google.com with code 80.
get("localhost", 8080) # Talks to our locally hosted server -> The HOST and PORT are specified in the echo.server.py file.
