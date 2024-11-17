import json

def validar_json(body):
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return None

def validar_campos_obrigatorios(body_json, campos_necessarios):
    return all(campo in body_json for campo in campos_necessarios)

def validar_nome_arquivo(nome):
    return isinstance(nome, str) and nome.strip() != ''

def validar_tipo_mime(tipo):
    mime_types_validos = ['text/plain', 'text/html']
    return tipo in mime_types_validos