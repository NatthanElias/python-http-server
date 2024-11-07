import socket
from File import File

# file = File('doc1', 'asdansodnas', 'text/type')

# print(f'Created file: {file.name}')

class Server:
    def __init__(self, host, port, data_payload = 2048):
        self.host = host
        self.port = port
        self.data_payload = data_payload

    def create_socket(type):
        if type is 'TCP':
            # Create a TCP socket
            sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
            # Enable reuse address/port 
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return sock
        else:
            return False
        
    def bind_socket(self, sock):
        server_address = (self.host, self.port)
        print ("Starting up echo server  on %s port %s" % server_address)
        sock.bind(server_address)

    

    
