from dataclasses import dataclass


@dataclass(frozen=True)
class PaginationParameters:
    limit: int
    offset: int
