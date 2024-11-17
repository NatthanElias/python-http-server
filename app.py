from server.server import Server

def main():
    server = Server('localhost', 8080)
    server.start_server()

if __name__ == '__main__':
    main()
