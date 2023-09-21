import socket

BYTES_TO_READ = 4096

def get(host, port):
  request = b"GET/ HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n"
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((host, port)) # Connect to server
  s.send(request) # Send request
  s.shutdown(socket.SHUT_WR) # "I'm done sending requests"
  result = s.recv(BYTES_TO_READ) # Keep reading incoming data (from server)
  while(len(result) > 0): # Keep reading the response until the sent response is empty.
    print(result)
    result = s.recv(BYTES_TO_READ)

  s.close()

#get("www.google.com", 80)
get("localhost", 8080)
