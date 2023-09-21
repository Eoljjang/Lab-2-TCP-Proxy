import socket

BYTES_TO_READ = 4096 # How much data you're willing to accept.

def get(host, port):
  request = b"GET/ HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n"
  # 1) Intialize socket
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

  # 2) Connect to server & make request
  s.connect((host, port)) 
  s.send(request)

  # 3) State that "you're done sending requests"
  s.shutdown(socket.SHUT_WR) 

  # 4) Continuously receiving the response from server.# Keep reading incoming data (from server)
  while(len(result) > 0): # Keep reading the response until the sent response is empty.
    print(result)
    result = s.recv(BYTES_TO_READ)

  # 5) Close the socket.
  s.close()

#get("www.google.com", 80) # GET function that makes a request to google.com with code 80.
get("localhost", 8080)
