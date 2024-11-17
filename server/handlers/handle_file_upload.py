from server.models.file import File
from server.models.storage import file_storage
from server.utils.authentication import validate_session_key
from server.utils.validations import (
    validar_json,
    validar_campos_obrigatorios,
    validar_nome_arquivo,
    validar_tipo_mime
)
from server.utils.exceptions import (
    RequisicaoInvalida,
    NaoAutorizado,
    TipoNaoSuportado
)
from server.handlers.handle_server_error import handle_server_error
from server.utils.response_helpers import gerar_resposta_http
from server.utils.parse_headers import parse_headers

def handle_file_upload(request, client_socket):
    try:
        # Extrai os headers e o corpo da requisição
        headers_part, body = request.split("\r\n\r\n", 1)
        headers = parse_headers(headers_part)

        # Verifica a autorização
        auth_key = headers.get("Authorization")
        if not validate_session_key(auth_key):
            raise NaoAutorizado("Chave de sessão inválida ou ausente.")

        # Valida o JSON do corpo da requisição
        body_json = validar_json(body)
        if body_json is None:
            raise RequisicaoInvalida("Corpo da requisição não é um JSON válido.")

        # Verifica se todos os campos obrigatórios estão presentes
        campos_necessarios = ['nome', 'conteudo', 'tipo']
        if not validar_campos_obrigatorios(body_json, campos_necessarios):
            raise RequisicaoInvalida("Campos obrigatórios faltando no corpo da requisição.")

        # Extrai os dados do corpo
        name = body_json.get("nome")
        content = body_json.get("conteudo")
        file_type = body_json.get("tipo")

        # Valida os campos individuais
        if not validar_nome_arquivo(name):
            raise RequisicaoInvalida("Nome de arquivo inválido.")

        if not validar_tipo_mime(file_type):
            raise TipoNaoSuportado(f"Tipo MIME '{file_type}' não suportado.")

        # Cria ou atualiza o arquivo
        file_storage[name] = File(name, content, file_type)
        response = gerar_resposta_http(
            201,
            "Created",
            "Arquivo criado/atualizado com sucesso",
            {"Content-Type": "text/plain", "Connection": "close"}
        )
        client_socket.send(response)
        client_socket.close()
        print(f"Arquivo {name} criado/atualizado com sucesso.")

    except NaoAutorizado as e:
        response = gerar_resposta_http(
            401,
            "Unauthorized",
            f"Erro: {str(e)}",
            {"Content-Type": "text/plain", "Connection": "close"}
        )
        client_socket.send(response)
        client_socket.close()
        print("Acesso não autorizado:", e)

    except RequisicaoInvalida as e:
        response = gerar_resposta_http(
            400,
            "Bad Request",
            f"Erro: {str(e)}",
            {"Content-Type": "text/plain", "Connection": "close"}
        )
        client_socket.send(response)
        client_socket.close()
        print("Requisição inválida:", e)

    except TipoNaoSuportado as e:
        response = gerar_resposta_http(
            415,
            "Unsupported Media Type",
            f"Erro: {str(e)}",
            {"Content-Type": "text/plain", "Connection": "close"}
        )
        client_socket.send(response)
        client_socket.close()
        print("Tipo não suportado:", e)

    except Exception as e:
        print("Erro ao processar o upload de arquivo:", e)
        handle_server_error(client_socket)