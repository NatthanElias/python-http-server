import json
from server.utils.authentication import authenticate
from server.handlers.handle_server_error import handle_server_error
from server.utils.response_helpers import gerar_resposta_http

def handle_login(request, client_socket):
    try:
        # Obtém o corpo da requisição
        body = request.split("\r\n\r\n", 1)[1]
        # Converte o corpo da requisição para um dicionário
        body_json = json.loads(body)

        username = body_json.get("username")
        password = body_json.get("password")

        # Autentica o usuário
        session_key = authenticate(username, password)

        if session_key:
            # Retorna a chave de sessão em caso de sucesso
            response_body = json.dumps({"key": session_key})
            response_headers = {
                "Content-Type": "application/json",
                "Connection": "close"
            }
            response = gerar_resposta_http(
                200,
                "OK",
                response_body,
                response_headers
            )
            print("Login bem-sucedido, chave de sessão enviada.")
        else:
            # Retorna erro de autenticação
            response = gerar_resposta_http(
                403,
                "Forbidden",
                "Credenciais inválidas",
                {"Content-Type": "text/plain", "Connection": "close"}
            )
            print("Falha no login, credenciais inválidas.")

        client_socket.send(response)
        client_socket.close()
    except Exception as e:
        print("Erro ao processar o login:", e)
        handle_server_error(client_socket)