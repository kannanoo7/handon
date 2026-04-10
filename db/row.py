class Row:

    def __init__(self, id, username):
        self.id = id
        self.username = username

    def __str__(self):
        return f"{self.id} {self.username}"