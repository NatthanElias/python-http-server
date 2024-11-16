# import socket
# import json
# import time
# from server.Server import Server
# from httptools import HttpRequestParser
# from server.File import File

# valid_username = "admin"  # Nome de usuário fixo
# valid_password = "senha123"  # Senha fixa
# valid_key = None  # Variável global para armazenar a chave de sessão

# class RequestHandler:
#     def __init__(self, client_socket):
#         self.client_socket = client_socket
#         self.parser = HttpRequestParser(self)  # Usando o parser para processar a requisição
#         self.url = None
#         self.method = None

#     def on_url(self, url):
#         # Extrai e decodifica a URL
#         self.url = url.decode()
#         print(f"URL recebida: {self.url}")  # Confirma que a URL foi recebida
    
#     def on_method(self, method):
#         # Captura o método HTTP (GET, POST, etc.)
#         self.method = method.decode()
#         print(f"Método HTTP: {self.method}")  # Confirma o método HTTP
    
#     def on_headers_complete(self):
#         print("Headers completos")  # Confirma que headers foram processados

#         # Verifica se a requisição é um POST para /login
#         if self.method == "POST" and self.url == "/login":
#             self.handle_login()
#         elif self.url and self.url.startswith("/arquivos/"):
#             file_name = self.url.split("/arquivos/")[-1]
#             file_name = file_name.rstrip('/')
#             print(f"Solicitação para o arquivo: {file_name}")  # Confirma o arquivo
#             self.handle_get(file_name)

#     def handle_get(self, file_name):
#         # Interage com o servidor para buscar o arquivo
#         file_storage = {
#             "doc1": File('doc1', 'Conteúdo do documento 1', 'text/plain'),
#             "doc2": File('doc2', 'Conteúdo do documento 2', 'text/plain')
#         }

#         if file_name in file_storage:
#             file = file_storage[file_name]
#             content = file.content
#             response = (
#                 "HTTP/1.1 200 OK\r\n"
#                 f"Content-Type: {file.type}\r\n"
#                 "Content-Length: " + str(len(content)) + "\r\n"
#                 "Connection: close\r\n\r\n" +
#                 content
#             )
#             print(f"Arquivo {file_name} encontrado, retornando 200 OK")  # Confirma 200 OK
#         else:
#             response = (
#                 "HTTP/1.1 404 Not Found\r\n"
#                 "Content-Type: text/plain\r\n"
#                 "Connection: close\r\n\r\n"
#                 "Error: File not found"
#             )
#             print(f"Arquivo {file_name} não encontrado, retornando 404")  # Confirma 404 Not Found

#         self.client_socket.send(response.encode('utf-8'))
#         self.client_socket.close()

#     def handle_login(self):
#         print("Handling login request...")
#         start_time = time.time()  # Marca o tempo de início
#         timeout = 10  # Tempo limite de 10 segundos para ler os dados da requisição
#         request = ""

#         while time.time() - start_time < timeout:
#             try:
#                 data = self.client_socket.recv(2048).decode('utf-8')  # Recebe o conteúdo da requisição
#                 if data:
#                     request += data
#                     break
#             except socket.timeout:
#                 continue
        
#         if not request:
#             response = (
#                 "HTTP/1.1 408 Request Timeout\r\n"
#                 "Content-Type: text/plain\r\n"
#                 "Connection: close\r\n\r\n"
#                 "Error: Request Timeout"
#             )
#             self.client_socket.send(response.encode('utf-8'))
#             self.client_socket.close()
#             print("Request timed out, closing connection.")
#             return

#         headers, body = request.split("\r\n\r\n", 1)
        
#         try:
#             login_data = json.loads(body)
#             print(f"Received login data: {login_data}")  # Log para ver os dados recebidos
#             username = login_data.get("username")
#             password = login_data.get("password")

#             if username == valid_username and password == valid_password:
#                 # Gerar chave de sessão e responder
#                 global valid_key
#                 valid_key = "sessionkey123"  # Chave gerada de forma simples
#                 response_body = json.dumps({"key": valid_key})
#                 response = (
#                     "HTTP/1.1 200 OK\r\n"
#                     "Content-Type: application/json\r\n"
#                     "Connection: close\r\n"
#                     f"Content-Length: {len(response_body)}\r\n\r\n"
#                     f"{response_body}"
#                 )
#                 print("Login successful, responding with key.")
#             else:
#                 response = (
#                     "HTTP/1.1 403 Forbidden\r\n"
#                     "Content-Type: text/plain\r\n"
#                     "Connection: close\r\n\r\n"
#                     "Error: Invalid username or password"
#                 )
#                 print("Login failed, invalid credentials.")
#         except json.JSONDecodeError:
#             response = (
#                 "HTTP/1.1 400 Bad Request\r\n"
#                 "Content-Type: text/plain\r\n"
#                 "Connection: close\r\n\r\n"
#                 "Error: Invalid JSON format"
#             )
#             print("Error: Invalid JSON format.")

#         self.client_socket.send(response.encode('utf-8'))
#         self.client_socket.close()
#         print("Response sent.")


# def main():
#     # Inicializa o servidor
#     serv = Server('localhost', 8080)  # Verifique a porta correta (8080 ou 80)
#     sock = serv.create_socket('TCP')
#     if not sock:
#         print('ERROR: Only TCP allowed')
#         return
#     serv.bind_socket(sock)

#     # Inicia o servidor e processa as requisições
#     sock.listen(5)
#     print("Server is listening on port 8080")

#     while True:
#         client_socket, _ = sock.accept()
#         client_socket.settimeout(10)  # Timeout de 10 segundos para a conexão
#         request_handler = RequestHandler(client_socket)
        
#         # Recebe a requisição e processa com HttpRequestParser
#         data = client_socket.recv(2048)
#         if data:
#             request_handler.parser.feed_data(data)  # Alimenta o parser com a requisição
#         else:
#             client_socket.close()


# if __name__ == '__main__':
#     main()

from server.server import Server

def main():
    server = Server('localhost', 8080)
    server.start_server()

if __name__ == '__main__':
    main()
