class NotFoundException(Exception): ...


class DuplicateException(Exception):
    def __init__(self, field: str) -> None:
        self.field = field
        super().__init__(f"Duplicate value for field {field}")
