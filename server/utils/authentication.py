VALID_USERNAME = "admin"
VALID_PASSWORD = "senha123"
VALID_SESSION_KEY = "sessionkey123"  # Depois implementar uma geração dinâmica de chave

def authenticate(username, password):
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        # Geração de uma chave de sessão ou token (para demonstração)
        return VALID_SESSION_KEY
    else:
        return None

def validate_session_key(key):
    return key == VALID_SESSION_KEY # Ou outra logica