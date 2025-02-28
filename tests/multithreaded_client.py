import threading
import requests

def send_requests(thread_id):
    try:
        # Fazer login e obter a chave de sessão
        login_response = requests.post(
            'http://localhost:8080/login',
            json={'username': 'admin', 'password': 'senha123'}
        )
        session_key = login_response.json().get('key')

        # Verifica se o login foi bem-sucedido
        if not session_key:
            print(f"Thread {thread_id}: Falha no login")
            return

        headers = {'Authorization': session_key}

        # Enviar requisição POST para criar um novo arquivo
        file_data = {
            'nome': f'arquivo_{thread_id}.txt',
            'conteudo': f'Conteúdo do arquivo {thread_id}',
            'tipo': 'text/plain'
        }
        post_response = requests.post(
            'http://localhost:8080/arquivos',
            headers=headers,
            json=file_data
        )
        print(f"Thread {thread_id}: POST /arquivos - Status {post_response.status_code}")

        # Enviar requisição GET para obter o arquivo criado
        get_response = requests.get(f"http://localhost:8080/arquivos/arquivo_{thread_id}.txt")
        print(f"Thread {thread_id}: GET /arquivos/arquivo_{thread_id}.txt - Status {get_response.status_code}")

    except Exception as e:
        print(f"Thread {thread_id}: Erro - {e}")

# Número de threads que você deseja criar
num_threads = 10

threads = []

for i in range(num_threads):
    thread = threading.Thread(target=send_requests, args=(i,))
    threads.append(thread)
    thread.start()

# Aguarda todas as threads terminarem
for thread in threads:
    thread.join()

print("Teste de multithreading concluído.")
