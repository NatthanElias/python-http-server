def parse_headers(headers_part):
    headers = {}
    lines = headers_part.split("\r\n")[1:]  # Ignora a linha de requisição
    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key.strip()] = value.strip()
    return headers