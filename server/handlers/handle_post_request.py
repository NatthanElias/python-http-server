from server.handlers.handle_file_upload import handle_file_upload
from server.handlers.handle_not_found import handle_not_found
from server.handlers.handle_server_error import handle_server_error

def handle_post_request(request, client_socket):
    try:
        request_line = request.splitlines()[0]
        method, path, _ = request_line.split()

        print(f"Caminho da requisição: {path}")

        if path == "/arquivos":  # Rota para inserir arquivos
            handle_file_upload(request, client_socket)
        else:
            handle_not_found(request, client_socket)
    except Exception as e:
        print("Erro ao processar a requisição POST:", e)
        handle_server_error(client_socket)