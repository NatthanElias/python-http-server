from server.Server import Server
from httptools import HttpRequestParser
from server.File import File

class RequestHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.parser = HttpRequestParser(self)
        self.url = None

    def on_url(self, url):
        # Extrai e decodifica a URL
        self.url = url.decode()
        print(f"URL recebida: {self.url}")
    
    def on_headers_complete(self):
        # Verifica se é uma requisição GET
        if self.url and self.url.startswith("/arquivos/"):
            file_name = self.url.split("/arquivos/")[-1]
            self.handle_get(file_name)

    def handle_get(self, file_name):
        # Interage com o servidor para buscar o arquivo
        file_storage = {
            "doc1": File('doc1', 'Conteúdo do documento 1', 'text/plain'),
            "doc2": File('doc2', 'Conteúdo do documento 2', 'text/plain')
        }

        if file_name in file_storage:
            file = file_storage[file_name]
            content = file.content
            response = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {file.file_type}\r\n"
                "Content-Length: " + str(len(content)) + "\r\n"
                "Connection: close\r\n\r\n" +
                content
            )
        else:
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                "Connection: close\r\n\r\n"
                "Error: File not found"
            )

        self.client_socket.send(response.encode('utf-8'))
        self.client_socket.close()

def main():
    # Inicializa o servidor
    serv = Server('localhost', 80)
    socket = serv.create_socket('TCP')
    if not socket:
        print('ERROR: Only TCP allowed')
        return
    serv.bind_socket(socket)

    # Inicia o servidor e processa as requisições
    socket.listen(5)
    print("Server is listening on port 80")

    while True:
        client_socket, _ = socket.accept()
        request_handler = RequestHandler(client_socket)
        
        # Recebe a requisição e processa com HttpRequestParser
        data = client_socket.recv(2048)
        if data:
            request_handler.parser.feed_data(data)
        else:
            client_socket.close()

if __name__ == '__main__':
    main()
