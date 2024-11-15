import socket
from server.File import File

# Simulando armazenamento de arquivos em memória
file_storage = {
    "doc1": File('doc1', 'Conteúdo do documento 1', 'text/plain'),
    "doc2": File('doc2', 'Conteúdo do documento 2', 'text/plain')
}

class Server:
    def __init__(self, host, port, data_payload=2048):
        self.host = host
        self.port = port
        self.data_payload = data_payload

    @staticmethod
    def create_socket(type):
        if type == 'TCP':
            # Criando um socket TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Habilita reuso de endereço/porta
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return sock
        else:
            return False
        
    def bind_socket(self, sock):
        server_address = (self.host, self.port)
        print("Starting up server on %s port %s" % server_address)
        sock.bind(server_address)

    def handle_request(self, client_socket):
        # Recebe a requisição do cliente
        request = client_socket.recv(self.data_payload).decode('utf-8')
        
        if request.startswith("GET"):
            # Extrai o nome do arquivo a partir do caminho na requisição
            try:
                request_line = request.splitlines()[0]
                method, path, _ = request_line.split()
                file_name = path.split("/arquivos/")[-1] if "/arquivos/" in path else None
                print(file_name)
                
                # Busca o arquivo em memória
                if file_name in file_storage:
                    content = file.content  # Acessa o conteúdo do arquivo
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        f"Content-Type: {file.file_type}\r\n"
                        "Content-Length: " + str(len(content)) + "\r\n"
                        "Connection: close\r\n\r\n" +
                        content
                    )
                else:
                    # Arquivo não encontrado
                    response = (
                        "HTTP/1.1 404 Not Found\r\n"
                        "Content-Type: text/plain\r\n"
                        "Connection: close\r\n\r\n"
                        "Error: File not found"
                    )

                # Envia a resposta
                client_socket.send(response.encode('utf-8'))
                print(f"Served file '{file_name}' with status: {'200 OK' if file_name in file_storage else '404 Not Found'}")
            except Exception as e:
                print("Error processing request:", e)
        
        # Fecha a conexão
        client_socket.close()

    def start_server(self):
        # Cria e configura o socket do servidor
        sock = self.create_socket('TCP')
        if sock:
            self.bind_socket(sock)
            sock.listen(5)
            print("Server is listening...")

            while True:
                print("Waiting to receive request from client")
                client_socket, address = sock.accept()
                self.handle_request(client_socket)
