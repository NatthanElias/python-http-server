from server.controllers.request_handler import (
    handle_get_request,
    handle_post_request,
    handle_login,
    handle_not_found
)

def route_request(method, path):
    if method == 'GET' and path.startswith('/arquivos/'):
        return handle_get_request
    elif method == 'POST' and path == '/login':
        return handle_login
    elif method == 'POST' and path == '/arquivos':
        return handle_post_request
    else:
        return handle_not_found
