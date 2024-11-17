from server.utils.response_helpers import gerar_resposta_http

def handle_not_found(request, client_socket):
    response = gerar_resposta_http(
        404,
        "Not Found",
        "Erro: Rota não encontrada",
        {"Content-Type": "text/plain", "Connection": "close"}
    )
    client_socket.send(response)
    client_socket.close()
    print("Rota não encontrada, retornando 404.")