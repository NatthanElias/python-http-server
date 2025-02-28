class File:

    def __init__(self, name, content, type):
        self.name = name
        self.content = content
        self.type = type

        # Validação do tipo (MIME types) está sendo feita na requisição POST