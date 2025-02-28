def gerar_resposta_http(status_code, status_message, body='', headers=None):
    if headers is None:
        headers = {}
    status_line = f"HTTP/1.1 {status_code} {status_message}\r\n"
    headers_lines = ''.join(f"{key}: {value}\r\n" for key, value in headers.items())
    blank_line = "\r\n"
    response = (status_line + headers_lines + blank_line + body).encode('utf-8')
    return response