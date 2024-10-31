class File:

    def __init__(self, name, content, type):
        self.name = name
        self.content = content
        self.type = type

        # validar tipo (MIME types)