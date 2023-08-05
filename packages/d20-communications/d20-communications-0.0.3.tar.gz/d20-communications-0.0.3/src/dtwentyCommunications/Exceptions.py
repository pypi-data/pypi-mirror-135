class UserNotFoundException(Exception):
    """Raised when user is not found"""

    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)

class ObjectNotFoundException(Exception):
    """Raised when object is not found"""

    def __init__(self, message="Object not found"):
        self.message = message
        super().__init__(self.message)
        
class MissingRequiredParametersException(Exception):
    """Raised when a duplicate user key is being inserted"""

    def __init__(self, message="requirements for request not complete"):
        self.message = message
        super().__init__(self.message)

class NotInsertedException(Exception):
    """Raised when an object cannot be inserted"""

    def __init__(self, message="Object was not inserted"):
        self.message = message
        super().__init__(self.message)

class NotUpdatedException(Exception):
    """Raised when an object cannot be updated"""

    def __init__(self, message="Object was not updated"):
        self.message = message
        super().__init__(self.message)

class NotDeletedException(Exception):
    """Raised when an object cannot be deleted"""

    def __init__(self, message="Object was not deleted"):
        self.message = message
        super().__init__(self.message)

class InvalidTokenException(Exception):
    """Raised when a token is not valid for an action"""

    def __init__(self, message="Provided token is not valid for", action="action"):
        self.message = f'{message} {action}'
        super().__init__(self.message)

    # def __str__(self):
    #     return f'{self.salary} -> {self.message}'