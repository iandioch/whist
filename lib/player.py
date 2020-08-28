class Player:
    def __init__(self, identifier):
        self.identifier = identifier

    def __hash__(self):
        return hash(self.identifier)

    def __eq__(self, other):
        return self.identifier == other.identifier
