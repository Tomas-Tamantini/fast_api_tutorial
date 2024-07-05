from typing import Protocol
from dataclasses import dataclass


class Authorization(Protocol):
    def has_permission(self, actor_id: int) -> bool: ...


@dataclass(frozen=True)
class DeleteAccountAuthorization:
    target_id: int

    def has_permission(self, actor_id: int) -> bool:
        return actor_id == self.target_id


@dataclass(frozen=True)
class UpdateAccountAuthorization(DeleteAccountAuthorization):
    pass
