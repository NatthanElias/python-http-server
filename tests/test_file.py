from server.models.file import File

file = File('doc1', 'asdansodnas', 'text/type')

print(f'Created file: {file.name}')