from server.utils.response_helpers import gerar_resposta_http

def handle_server_error(client_socket):
    response = gerar_resposta_http(
        500,
        "Internal Server Error",
        "Erro Interno do Servidor",
        {"Content-Type": "text/plain", "Connection": "close"}
    )
    client_socket.send(response)
    client_socket.close()
    print("Erro interno do servidor, retornando 500.")