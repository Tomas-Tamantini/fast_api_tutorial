from fast_api_tutorial.security import Authorization


def test_only_user_can_delete_their_own_account():
    auth = Authorization()
    assert auth.can_delete_account(actor_id=1, target_id=1)
    assert not auth.can_delete_account(actor_id=1, target_id=2)


def test_only_user_can_update_their_own_account():
    auth = Authorization()
    assert auth.can_update_account(actor_id=1, target_id=1)
    assert not auth.can_update_account(actor_id=1, target_id=2)
