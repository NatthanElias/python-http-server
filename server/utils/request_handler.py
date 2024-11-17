import json
from server.models.file import File
from server.utils.authentication import authenticate, validate_session_key

# Simulando armazenamento de arquivos em memória
file_storage = {
    "doc1": File('doc1', 'Conteúdo do documento 1', 'text/plain'),
    "doc2": File('doc2', 'Conteúdo do documento 2', 'text/plain')
}

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
            # Certifique-se de que o conteúdo é codificado corretamente
            content_bytes = content.encode('utf-8')
            response_headers = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {file.type}\r\n"
                f"Content-Length: {len(content_bytes)}\r\n"
                "Connection: close\r\n"
                "\r\n"
            )
            # Concatena os headers e o conteúdo em bytes
            response = response_headers.encode('utf-8') + content_bytes
            print("Resposta sendo enviada:\n", response_headers + content)
        else:
            response_body = "Erro: Arquivo não encontrado"
            response_headers = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
                "Connection: close\r\n"
                "\r\n"
            )
            response = response_headers.encode('utf-8') + response_body.encode('utf-8')
            print(f"Erro: {file_name} não encontrado em file_storage.")

        client_socket.send(response)
        client_socket.close()
    except Exception as e:
        print("Erro ao processar a requisição GET:", e)
        handle_server_error(client_socket)

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
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json\r\n"
                "Connection: close\r\n\r\n" +
                json.dumps({"key": session_key})
            )
            print("Login bem-sucedido, chave de sessão enviada.")
        else:
            # Retorna erro de autenticação
            response = (
                "HTTP/1.1 403 Forbidden\r\n"
                "Content-Type: text/plain\r\n"
                "Connection: close\r\n\r\n"
                "Credenciais inválidas"
            )
            print("Falha no login, credenciais inválidas.")

        client_socket.send(response.encode('utf-8'))
        client_socket.close()
    except Exception as e:
        print("Erro ao processar o login:", e)
        handle_server_error(client_socket)

def handle_file_upload(request, client_socket):
    try:
        # Extrai os headers e o corpo da requisição
        headers_part, body = request.split("\r\n\r\n", 1)
        headers = parse_headers(headers_part)
        
        # Verifica a autorização
        auth_key = headers.get("Authorization")
        if not validate_session_key(auth_key):
            response = (
                "HTTP/1.1 401 Unauthorized\r\n"
                "Content-Type: text/plain\r\n"
                "Connection: close\r\n\r\n"
                "Erro: Não autorizado"
            )
            client_socket.send(response.encode('utf-8'))
            client_socket.close()
            print("Acesso não autorizado, chave de sessão inválida.")
            return

        # Verifica se todos os campos estão presentes
        campos_necessarios = ['nome', 'conteudo', 'tipo']
        if not all(campo in body_json for campo in campos_necessarios):
            # Retorna erro 400 Bad Request
            response = (
                "HTTP/1.1 400 Bad Request\r\n"
                "Content-Type: text/plain\r\n"
                "Connection: close\r\n\r\n"
                "Erro: Campos obrigatórios faltando no corpo da requisição"
            )
            client_socket.send(response.encode('utf-8'))
            client_socket.close()
            return

        # Processa o corpo da requisição
        body_json = json.loads(body)
        name = body_json.get("nome")
        content = body_json.get("conteudo")
        type = body_json.get("tipo")
        # Cria ou atualiza o arquivo
        file_storage[name] = File(name, content, type)
        response = (
            "HTTP/1.1 201 Created\r\n"
            "Content-Type: text/plain\r\n"
            "Connection: close\r\n\r\n"
            "Arquivo criado/atualizado com sucesso"
        )
        client_socket.send(response.encode('utf-8'))
        client_socket.close()
        print(f"Arquivo {name} criado/atualizado com sucesso.")
    except Exception as e:
        print("Erro ao processar o upload de arquivo:", e)
        handle_server_error(client_socket)

def handle_not_found(request, client_socket):
    response = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/plain\r\n"
        "Connection: close\r\n\r\n"
        "Erro: Rota não encontrada"
    )
    client_socket.send(response.encode('utf-8'))
    client_socket.close()
    print("Rota não encontrada, retornando 404.")

def handle_server_error(client_socket):
    response = (
        "HTTP/1.1 500 Internal Server Error\r\n"
        "Content-Type: text/plain\r\n"
        "Connection: close\r\n\r\n"
        "Erro Interno do Servidor"
    )
    client_socket.send(response.encode('utf-8'))
    client_socket.close()
    print("Erro interno do servidor, retornando 500.")

def parse_headers(headers_part):
    headers = {}
    lines = headers_part.split("\r\n")[1:]  # Ignora a linha de requisição
    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value
    return headers