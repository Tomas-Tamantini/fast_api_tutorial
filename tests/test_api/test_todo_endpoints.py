from http import HTTPStatus
from fast_api_tutorial.exceptions import BadTokenError


def _make_create_request(client, request_body: dict, token="good_token"):
    return client.post(
        "/todos/", json=request_body, headers={"Authorization": f"Bearer {token}"}
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
