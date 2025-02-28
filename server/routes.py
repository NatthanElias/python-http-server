from server.handlers.handle_get_request import handle_get_request
from server.handlers.handle_post_request import handle_post_request
from server.handlers.handle_login import handle_login
from server.handlers.handle_not_found import handle_not_found
from server.handlers.handle_get_all_files import handle_get_all_files  # Novo import

def route_request(method, path):
    if method == 'GET' and path.startswith('/arquivos/'):
        return handle_get_request
    elif method == 'GET' and path == '/arquivos':
        return handle_get_all_files  # Nova rota para listar todos os arquivos
    elif method == 'POST' and path == '/arquivos':
        return handle_post_request
    elif method == 'POST' and path == '/login':
        return handle_login
    else:
        return handle_not_found