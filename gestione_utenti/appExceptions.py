class RowNotFoundException(Exception):
    def __init__(self, message="Row not found"):
        self.message = message
        super().__init__(self.message)


class AlreadyExistException(Exception):
    def __init__(self, message="User with that data already exists"):
        self.message = message
        super().__init__(self.message)
