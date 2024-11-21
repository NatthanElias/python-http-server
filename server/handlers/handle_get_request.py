from server.models.storage import file_storage
from server.handlers.handle_server_error import handle_server_error
from server.utils.response_helpers import gerar_resposta_http

def handle_get_request(request, client_socket):
    try:
        request_line = request.splitlines()[0]
        method, path, _ = request_line.split()

        print(f"Caminho da requisição: {path}")

        # Extrai o nome do arquivo
        file_name = path.split("/arquivos/", 1)[1] if "/arquivos/" in path else None

        print(f"Arquivo solicitado: {file_name}")

        if file_name and file_name in file_storage:
            file = file_storage[file_name]
            content = file.content
            content_bytes = content.encode('utf-8')
            response_headers = {
                "Content-Type": file.type,
                "Content-Length": str(len(content_bytes)),
                "Connection": "close"
            }
            response = gerar_resposta_http(
                200,
                "OK",
                content,
                response_headers
            )
            print("Resposta sendo enviada:\n", response.decode('utf-8'))
        else:
            response_body = "Erro: Arquivo não encontrado"
            response_headers = {
                "Content-Type": "text/plain",
                "Content-Length": str(len(response_body.encode('utf-8'))),
                "Connection": "close"
            }
            response = gerar_resposta_http(
                404,
                "Not Found",
                response_body,
                response_headers
            )
            print(f"Erro: {file_name} não encontrado em file_storage.")

        client_socket.send(response)
        client_socket.close()
    except Exception as e:
        print("Erro ao processar a requisição GET:", e)
        handle_server_error(client_socket)