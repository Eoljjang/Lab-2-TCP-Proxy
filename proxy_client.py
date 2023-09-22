# Proxy-client, basically the exact same as regular client.
import socket

BYTES_TO_READ = 4096 # How much data you're willing to accept.

def get(host, port):
  request = b"GET / HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n"
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Used a 'with' block isntead, so we don't have to call "s.close()"
    s.connect((host,port)) 
    s.send(request)
    s.shutdown(socket.SHUT_WR) 
    chunk = s.recv(BYTES_TO_READ) # Different part.
    result = b'' + chunk

    # 4) Continuously receiving the response from server.# Keep reading incoming data (from server)
    while(len(chunk) > 0): # Keep reading the response until the sent response is empty.
      chunk = s.recv(BYTES_TO_READ)
      result += chunk
    s.close()# Empty bytestring was sent
    return result

print(get("127.0.0.1", 8080))
