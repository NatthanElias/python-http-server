from server.Server import Server
from httptools import HttpRequestParser

class RequestHandler:
    def __init__(self):
        self.parser = HttpRequestParser(self)
    
    def on_url(self, url):
        print(f"URL recebida: {url.decode()}")

def main():
    # print("Testando o parsing HTTP")
    # handler = RequestHandler()
    # data = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
    # handler.parser.feed_data(data)
    serv = Server('localhost', 80)
    socket = serv.create_socket('TCP')
    if not socket:
        print('ERROR: Only TCP allowed')
    serv.bind_socket(socket)

    


if __name__ == '__main__':
    main()
