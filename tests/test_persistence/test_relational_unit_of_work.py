import pytest
from fast_api_tutorial.persistence.relational import RelationalUnitOfWork
from fast_api_tutorial.exceptions import DuplicateFieldError


def test_relational_unit_of_work_raises_duplicate_error_on_commit_if_user_already_exists(
    session, user_db_request
):
    uow = RelationalUnitOfWork(session_factory=lambda: session)
    with uow:
        uow.user_repository.add(user_db_request(username="test", email="a@b.com"))
        uow.user_repository.add(user_db_request(username="test", email="c@d.com"))
        with pytest.raises(DuplicateFieldError) as e:
            uow.commit()
        assert "username" in str(e)
