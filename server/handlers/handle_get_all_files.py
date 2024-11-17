import json
from server.models.storage import file_storage
from server.utils.response_helpers import gerar_resposta_http
from server.handlers.handle_server_error import handle_server_error

def handle_get_all_files(request, client_socket):
    try:
        # Verifica se há arquivos armazenados
        if not file_storage:
            response_body = {
                "mensagem": "Nenhum arquivo armazenado."
            }
        else:
            # Extrai a lista de nomes de arquivos do armazenamento
            file_names = list(file_storage.keys())
            response_body = {
                "arquivos": file_names
            }
        response_body_str = json.dumps(response_body)
        # Gera a resposta HTTP
        response_headers = {
            "Content-Type": "application/json",
            "Content-Length": str(len(response_body_str.encode('utf-8'))),
            "Connection": "close"
        }
        response = gerar_resposta_http(
            200,
            "OK",
            response_body_str,
            response_headers
        )
        client_socket.send(response)
        client_socket.close()
        print("Resposta enviada para GET /arquivos.")
    except Exception as e:
        print("Erro ao processar a requisição GET /arquivos:", e)
        handle_server_error(client_socket)