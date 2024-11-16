# import socket
# from server.models.file import File
# import json

# # Simulando armazenamento de arquivos em memória
# file_storage = {
#     "doc1": File('doc1', 'Conteúdo do documento 1', 'text/plain'),
#     "doc2": File('doc2', 'Conteúdo do documento 2', 'text/plain')
# }

# VALID_USERNAME = "admin"
# VALID_PASSWORD = "senha123"

# class Server:
#     def __init__(self, host, port, data_payload=2048):
#         self.host = host
#         self.port = port
#         self.data_payload = data_payload

#     @staticmethod
#     def create_socket(type):
#         if type == 'TCP':
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#             return sock
#         else:
#             return False

#     def bind_socket(self, sock):
#         server_address = (self.host, self.port)
#         print("Starting up server on %s port %s" % server_address)
#         sock.bind(server_address)
    
#     @staticmethod
#     def authenticate(username, password):
#         if username == VALID_USERNAME and password == VALID_PASSWORD:
#             # Geração de uma chave de sessão ou token (simples, para demonstração)
#             return "sessionkey123"
#         else:
#             return None

#     def handle_request(self, client_socket):
#         request = client_socket.recv(self.data_payload).decode('utf-8')
#         print("Request received:", request)  # Log do conteúdo da requisição
        
#         if request.startswith("GET"):
#             try:
#                 request_line = request.splitlines()[0]
#                 method, path, _ = request_line.split()
                
#                 print(f"Path from request: {path}")
                
#                 # Extrai o nome do arquivo
#                 file_name = path.split("/arquivos/")[-1] if "/arquivos/" in path else None

#                 print(f"File requested: {file_name}")
                
#                 if file_name and file_name in file_storage:
#                     file = file_storage[file_name]
#                     content = file.content
#                     response = (
#                         "HTTP/1.1 200 OK\r\n"
#                         f"Content-Type: {file.type}\r\n"
#                         "Content-Length: " + str(len(content)) + "\r\n"
#                         "Connection: close\r\n\r\n" +
#                         content
#                     )
#                 else:
#                     response = (
#                         "HTTP/1.1 404 Not Found\r\n"
#                         "Content-Type: text/plain\r\n"
#                         "Connection: close\r\n\r\n"
#                         "Error: File not found"
#                     )
#                     print(f"Error: {file_name} not found in file_storage.")

#                 client_socket.send(response.encode('utf-8'))
#             except Exception as e:
#                 print("Error processing request:", e)
        
#         elif request.startswith("POST"):
#             try:
#                 request_line = request.splitlines()[0]
#                 method, path, _ = request_line.split()

#                 print(f"Path from request: {path}")

#                 if path == "/login":  # Verifica se é a rota de login
#                     # Obtém o corpo da requisição
#                     body = request.split("\r\n\r\n", 1)[1]
#                     # Converte o corpo da requisição para um dicionário
#                     body_json = json.loads(body)

#                     username = body_json.get("username")
#                     password = body_json.get("password")

#                     # Autentica o usuário
#                     session_key = Server.authenticate(username, password)

#                     if session_key:
#                         # Retorna a chave de sessão em caso de sucesso
#                         response = (
#                             "HTTP/1.1 200 OK\r\n"
#                             "Content-Type: application/json\r\n"
#                             "Connection: close\r\n\r\n" +
#                             json.dumps({"key": session_key})
#                         )
#                     else:
#                         # Retorna erro de autenticação
#                         response = (
#                             "HTTP/1.1 403 Forbidden\r\n"
#                             "Content-Type: text/plain\r\n"
#                             "Connection: close\r\n\r\n"
#                             "Invalid credentials"
#                         )
#                 else:
#                     # Tratamento para outras rotas, como /arquivos/
#                     pass

#                 # Envia a resposta para o cliente
#                 client_socket.send(response.encode('utf-8'))
            
#             except Exception as e:
#                 print("Error processing request:", e)
#                 response = (
#                     "HTTP/1.1 500 Internal Server Error\r\n"
#                     "Content-Type: text/plain\r\n"
#                     "Connection: close\r\n\r\n"
#                     "Server Error"
#                 )
#                 client_socket.send(response.encode('utf-8'))

#         client_socket.close()

#     def start_server(self):
#         sock = self.create_socket('TCP')
#         if sock:
#             self.bind_socket(sock)
#             sock.listen(5)
#             print("Server is listening...")

#             while True:
#                 client_socket, address = sock.accept()
#                 self.handle_request(client_socket)

import socket
import threading
from server.routes import route_request

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
            sock.listen(5)
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
            from server.controllers.request_handler import handle_server_error
            handle_server_error(client_socket)