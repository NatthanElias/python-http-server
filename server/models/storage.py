from server.models.file import File

# Simulando armazenamento de arquivos em memória
file_storage = {
    "doc1": File('doc1', 'Conteúdo do documento 1', 'text/plain'),
    "doc2": File('doc2', 'Conteúdo do documento 2', 'text/plain')
}