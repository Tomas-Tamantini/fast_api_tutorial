import pytest
from sqlalchemy import select
from fast_api_tutorial.persistence.relational import RelationalUserRepository, User
from fast_api_tutorial.exceptions import NotFoundException


@pytest.mark.integration
def test_create_user_saves_it_to_db(session, user_request):
    repository = RelationalUserRepository(session)
    repository.add(user_request(username="test", email="a@b.com"))
    session.commit()
    user = session.scalar(select(User).where(User.username == "test"))
    assert user.username == "test"
    assert user.email == "a@b.com"
    assert user.id == 1


@pytest.mark.integration
def test_getting_inexistent_user_raises_not_found_error(session):
    repository = RelationalUserRepository(session)
    with pytest.raises(NotFoundException):
        repository.get_from_email("a@b.com")


@pytest.mark.integration
def test_getting_user_from_valid_email_returns_user(session, user_request):
    repository = RelationalUserRepository(session)
    repository.add(user_request(username="test", email="a@b.com"))
    session.commit()
    user = repository.get_from_email("a@b.com")
    assert user.username == "test"


@pytest.mark.integration
def test_getting_inexistent_user_by_id_raises_not_found_error(session):
    repository = RelationalUserRepository(session)
    with pytest.raises(NotFoundException):
        repository.get(id=1)


@pytest.mark.integration
def test_getting_user_by_id_returns_user(session, user_request):
    repository = RelationalUserRepository(session)
    repository.add(user_request(username="test"))
    session.commit()
    user = repository.get(id=1)
    assert user.username == "test"


@pytest.mark.integration
def test_get_all_returns_all_users(session, user_request):
    repository = RelationalUserRepository(session)
    repository.add(user_request(username="test 1", email="a@b.com"))
    repository.add(user_request(username="test 2", email="b@a.com"))
    session.commit()
    users = repository.get_all()
    assert len(users) == 2
    assert [user.username for user in users] == ["test 1", "test 2"]


@pytest.mark.integration
def test_update_inexistent_user_raises_not_found_error(session, user_request):
    repository = RelationalUserRepository(session)
    with pytest.raises(NotFoundException):
        repository.update(id=1, entity=user_request())


@pytest.mark.integration
def test_update_user_updates_user(session, user_request):
    repository = RelationalUserRepository(session)
    repository.add(user_request())
    session.commit()
    repository.update(
        id=1,
        entity=user_request(username="new", email="new@new.com"),
    )
    session.commit()
    user = repository.get(id=1)
    assert user.username == "new"
    assert user.email == "new@new.com"


@pytest.mark.integration
def test_delete_inexistent_user_raises_not_found_error(session):
    repository = RelationalUserRepository(session)
    with pytest.raises(NotFoundException):
        repository.delete(id=1)


@pytest.mark.integration
def test_delete_user_deletes_user(session, user_request):
    repository = RelationalUserRepository(session)
    repository.add(user_request())
    session.commit()
    repository.delete(id=1)
    session.commit()
    with pytest.raises(NotFoundException):
        repository.get(id=1)
