import pytest
from sqlalchemy import select
from fast_api_tutorial.persistence.relational import RelationalUserRepository, UserDB
from fast_api_tutorial.exceptions import NotFoundError


@pytest.mark.integration
def test_create_user_saves_it_to_db(session, user_db_request):
    repository = RelationalUserRepository(session)
    repository.add(user_db_request(username="test", email="a@b.com"))
    session.commit()
    user = session.scalar(select(UserDB).where(UserDB.username == "test"))
    assert user.username == "test"
    assert user.email == "a@b.com"
    assert user.id == 1


@pytest.mark.integration
def test_getting_user_not_in_db_raises_not_found_error(session):
    repository = RelationalUserRepository(session)
    with pytest.raises(NotFoundError):
        repository.get_from_email("a@b.com")


@pytest.mark.integration
def test_getting_user_from_db_with_valid_email_returns_user(session, user_db_request):
    repository = RelationalUserRepository(session)
    repository.add(user_db_request(username="test", email="a@b.com"))
    session.commit()
    user = repository.get_from_email("a@b.com")
    assert user.username == "test"


@pytest.mark.integration
def test_getting_user_by_id_not_in_db_raises_not_found_error(session):
    repository = RelationalUserRepository(session)
    with pytest.raises(NotFoundError):
        repository.get(id=1)


@pytest.mark.integration
def test_getting_user_by_id_in_db_returns_user(session, user_db_request):
    repository = RelationalUserRepository(session)
    repository.add(user_db_request(username="test"))
    session.commit()
    user = repository.get(id=1)
    assert user.username == "test"


@pytest.mark.integration
def test_get_all_returns_all_users_in_db(session, user_db_request):
    repository = RelationalUserRepository(session)
    repository.add(user_db_request(username="test 1", email="a@b.com"))
    repository.add(user_db_request(username="test 2", email="b@a.com"))
    session.commit()
    users = repository.get_all()
    assert len(users) == 2
    assert [user.username for user in users] == ["test 1", "test 2"]


@pytest.mark.integration
def test_get_paginated_returns_users_in_page(session, user_db_request):
    repository = RelationalUserRepository(session)
    for i in range(1, 4):
        repository.add(user_db_request(username=f"test {i}", email=f"a{i}@b.com"))
    session.commit()
    users = repository.get_paginated(page=2, size=2)
    assert len(users) == 1
    assert users[0].username == "test 3"


@pytest.mark.integration
def test_update_user_not_in_db_raises_not_found_error(session, user_db_request):
    repository = RelationalUserRepository(session)
    with pytest.raises(NotFoundError):
        repository.update(id=1, entity=user_db_request())


@pytest.mark.integration
def test_update_user_in_db_updates_fields(session, user_db_request):
    repository = RelationalUserRepository(session)
    repository.add(user_db_request())
    session.commit()
    repository.update(
        id=1,
        entity=user_db_request(username="new", email="new@new.com"),
    )
    session.commit()
    user = repository.get(id=1)
    assert user.username == "new"
    assert user.email == "new@new.com"


@pytest.mark.integration
def test_delete_user_not_in_db_raises_not_found_error(session):
    repository = RelationalUserRepository(session)
    with pytest.raises(NotFoundError):
        repository.delete(id=1)


@pytest.mark.integration
def test_delete_user_in_db_removes_it(session, user_db_request):
    repository = RelationalUserRepository(session)
    repository.add(user_db_request())
    session.commit()
    repository.delete(id=1)
    session.commit()
    with pytest.raises(NotFoundError):
        repository.get(id=1)
