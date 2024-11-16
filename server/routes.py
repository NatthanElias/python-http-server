from controllers.request_handler import handle_get_file, handle_post_file
from controllers.authentication import handle_login

routes = {
    ('GET', '/arquivos/'): handle_get_file,
    ('POST', '/arquivos/'): handle_post_file,
    ('POST', '/login'): handle_login,
}