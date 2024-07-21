from http import HTTPStatus
from fast_api_tutorial.exceptions import BadTokenError, NotFoundError


def _make_create_request(client, request_body: dict, token="good_token"):
    return client.post(
        "/todos/", json=request_body, headers={"Authorization": f"Bearer {token}"}
    )


def _make_delete_request(client, todo_id: int = 1, token="good_token"):
    return client.delete(
        f"/todos/{todo_id}", headers={"Authorization": f"Bearer {token}"}
    )


def test_create_todo_returns_unauthorized_if_no_token(client):
    response = client.post("/todos/", json={}, headers={})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_create_todo_returns_unauthorized_if_bad_token(
    client, jwt_builder, valid_todo_request
):
    jwt_builder.get_token_subject.side_effect = BadTokenError
    response = _make_create_request(client, valid_todo_request, token="bad_token")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert jwt_builder.get_token_subject.call_args[0][0] == "bad_token"


def test_create_invalid_todo_returns_unprocessable_entity(client):
    response = _make_create_request(client, request_body={"bad": "body"})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_valid_todo_returns_created(client, valid_todo_request):
    response = _make_create_request(client, valid_todo_request)
    assert response.status_code == HTTPStatus.CREATED


def test_create_valid_todo_returns_created_todo_response(client, valid_todo_request):
    response = _make_create_request(client, valid_todo_request)
    assert response.json() == {
        "id": 1,
        "title": valid_todo_request["title"],
        "description": valid_todo_request["description"],
        "status": valid_todo_request["status"],
    }


def test_create_valid_todo_delegates_storage_to_repository(
    client, valid_todo_request, todo_repository
):
    _make_create_request(client, valid_todo_request)
    assert todo_repository.add.call_args[0][0].title == valid_todo_request["title"]
    assert (
        todo_repository.add.call_args[0][0].description
        == valid_todo_request["description"]
    )
    assert todo_repository.add.call_args[0][0].status == valid_todo_request["status"]


def test_create_valid_todo_stores_todo_with_user_id(
    client, valid_todo_request, todo_repository, user_repository, user_response
):
    user_repository.get_from_email.return_value = user_response(id=123)
    _make_create_request(client, valid_todo_request)
    assert todo_repository.add.call_args[0][0].user_id == 123


def test_create_valid_todo_commits_changes(client, valid_todo_request, unit_of_work):
    _make_create_request(client, valid_todo_request)
    assert unit_of_work.commit.called


def test_delete_todo_returns_unauthorized_if_no_token(client):
    response = client.delete("/todos/1", headers={})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_todo_returns_unauthorized_if_bad_token(client, jwt_builder):
    jwt_builder.get_token_subject.side_effect = BadTokenError
    response = _make_delete_request(client, token="bad_token")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert jwt_builder.get_token_subject.call_args[0][0] == "bad_token"


def test_delete_todo_returns_not_found_if_todo_does_not_exist(client, todo_repository):
    todo_repository.delete.side_effect = NotFoundError
    response = _make_delete_request(client)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_todo_returns_forbidden_if_user_does_not_have_authorization(
    client, authorization
):
    authorization.has_permission.return_value = False
    response = _make_delete_request(client)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_todo_delegates_storage_to_repository(client, todo_repository):
    _make_delete_request(client, todo_id=123)
    assert todo_repository.delete.call_args[0][0] == 123
