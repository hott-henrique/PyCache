""" PyCache Exceptions Module. """

class InexistentCacheAccess(Exception):
    """Raised when trying to access an inexistent cache."""

    def __init__(self, *args: object) -> None:
        super().__init__(f'Trying to access an inexistent cache. Cache: {args[0]}. Client {args[1]}.')

class ExistentCacheCreation(Exception):
    """Raised when trying to overwrite an existent cache."""

    def __init__(self, *args: object) -> None:
        super().__init__(f'Trying to create an existent cache. Cache: {args[0]}. Client: {args[1]}.')

class InexistentObjectAccess(Exception):
    """Raised when trying to access an inexistent object."""

    def __init__(self, *args: object) -> None:
        super().__init__(f'Trying to access an inexistent object. Object: {args[0]}. Cache: {args[1]}. Client: {args[2]}.')

class ExistentObjectCreation(Exception):
    """Raised when trying to overwrite an existent object."""

    def __init__(self, *args: object) -> None:
        super().__init__(f'Trying to create an existent object. Object: {args[0]}. Cache {args[1]}. Client {args[2]}.')
