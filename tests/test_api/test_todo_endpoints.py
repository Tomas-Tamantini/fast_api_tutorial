from http import HTTPStatus
from typing import Optional
from fast_api_tutorial.exceptions import BadTokenError, NotFoundError
from fast_api_tutorial.persistence.models import PaginationParameters


def _make_create_request(client, request_body: dict, token="good_token"):
    return client.post(
        "/todos/", json=request_body, headers={"Authorization": f"Bearer {token}"}
    )


def _make_delete_request(client, todo_id: int = 1, token="good_token"):
    return client.delete(
        f"/todos/{todo_id}", headers={"Authorization": f"Bearer {token}"}
    )


def _make_get_request(
    client,
    limit: int = 10,
    offset: int = 0,
    status: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    token="good_token",
):
    query_params = {"limit": limit, "offset": offset}
    if status:
        query_params["status"] = status
    if title:
        query_params["title"] = title
    if description:
        query_params["description"] = description
    return client.get(
        "/todos/", headers={"Authorization": f"Bearer {token}"}, params=query_params
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
    response = _make_create_request(client, valid_todo_request).json()
    assert response["title"] == valid_todo_request["title"]
    assert response["description"] == valid_todo_request["description"]
    assert response["status"] == valid_todo_request["status"]
    assert "created_at" in response
    assert "id" in response
    assert "updated_at" in response


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


def test_get_todos_returns_unauthorized_if_no_token(client):
    response = client.get("/todos/", headers={})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_todos_returns_unauthorized_if_bad_token(client, jwt_builder):
    jwt_builder.get_token_subject.side_effect = BadTokenError
    response = _make_get_request(client, token="bad_token")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert jwt_builder.get_token_subject.call_args[0][0] == "bad_token"


def test_get_todos_returns_paginated_todos(client, todo_repository, todo_response):
    todo = todo_response()
    todo_repository.get_paginated.return_value = [todo]
    response = _make_get_request(client, limit=10, offset=0).json()
    assert len(response["todos"]) == 1
    retrieved = response["todos"][0]
    assert "user_id" not in retrieved
    todo_json = todo.model_dump()
    assert retrieved["id"] == todo_json["id"]
    assert retrieved["title"] == todo_json["title"]
    assert todo_repository.get_paginated.call_args[0][0] == PaginationParameters(
        limit=10, offset=0
    )


def test_get_todos_returns_only_todos_owned_by_user(
    client, todo_repository, user_repository, user_response
):
    user_repository.get_from_email.return_value = user_response(id=123)
    _make_get_request(client)
    assert todo_repository.get_paginated.call_args[0][1].user_id == 123


def test_get_todos_filters_by_attributes(client, todo_repository):
    _make_get_request(client, status="pending", title="title")
    assert todo_repository.get_paginated.call_args[0][1].status == "pending"
    assert todo_repository.get_paginated.call_args[0][1].title == "title"
    assert todo_repository.get_paginated.call_args[0][1].description is None
