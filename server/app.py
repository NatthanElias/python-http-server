from httptools import HttpRequestParser

class RequestHandler:
    def __init__(self):
        self.parser = HttpRequestParser(self)
    
    def on_url(self, url):
        print(f"URL recebida: {url.decode()}")

def main():
    print("Testando o parsing HTTP")
    handler = RequestHandler()
    data = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
    handler.parser.feed_data(data)

if __name__ == '__main__':
    main()
