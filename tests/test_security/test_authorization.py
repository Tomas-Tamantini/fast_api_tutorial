from fast_api_tutorial.security import (
    DeleteAccountAuthorization,
    UpdateAccountAuthorization,
    DeleteTodoAuthorization,
)


def test_only_user_can_delete_their_own_account():
    action = UpdateAccountAuthorization(target_id=1)
    assert action.has_permission(actor_id=1)
    assert not action.has_permission(actor_id=2)


def test_only_user_can_update_their_own_account():
    action = DeleteAccountAuthorization(target_id=1)
    assert action.has_permission(actor_id=1)
    assert not action.has_permission(actor_id=2)


def test_only_user_can_delete_their_own_todo():
    action = DeleteTodoAuthorization(owner_id=1)
    assert action.has_permission(actor_id=1)
    assert not action.has_permission(actor_id=2)
