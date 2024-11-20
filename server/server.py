import socket
import threading
from server.routes import route_request
from server.handlers.handle_server_error import handle_server_error

class Server:
    def __init__(self, host, port, data_payload=2048):
        self.host = host
        self.port = port
        self.data_payload = data_payload

    @staticmethod
    def create_socket(protocol):
        if protocol == 'TCP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return sock
        else:
            return None

    def bind_socket(self, sock):
        server_address = (self.host, self.port)
        print("Iniciando servidor em %s porta %s" % server_address)
        sock.bind(server_address)

    def start_server(self):
        sock = self.create_socket('TCP')
        if sock:
            self.bind_socket(sock)
            sock.listen(50)
            print("Servidor está escutando...")

            while True:
                client_socket, address = sock.accept()
                # Trata a requisição em uma nova thread
                thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                thread.start()

    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(self.data_payload).decode('utf-8')
            request_line = request.splitlines()[0]
            method, path, _ = request_line.split()

            # Obter o manipulador adequado com base na rota
            handler = route_request(method, path)
            handler(request, client_socket)
        except Exception as e:
            print("Erro ao processar a requisição:", e)
            handle_server_error(client_socket)