class Signature:
    def __init__(self):
        self.name = None
        self.pattern = None
        self.found_offset = -1

    def __str__(self):
        return self.name
