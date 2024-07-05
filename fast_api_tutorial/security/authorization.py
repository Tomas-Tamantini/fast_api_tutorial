from typing import Protocol


class AuthorizationProtocol(Protocol):
    def can_delete_account(self, actor_id: int, target_id: int) -> bool: ...

    def can_update_account(self, actor_id: int, target_id: int) -> bool: ...


class Authorization:
    def can_delete_account(self, actor_id: int, target_id: int) -> bool:
        return actor_id == target_id

    def can_update_account(self, actor_id: int, target_id: int) -> bool:
        return actor_id == target_id
