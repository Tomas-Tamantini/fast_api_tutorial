from fast_api_tutorial.schemas import CreateUserRequest


def test_create_user_request_hashes_password():
    request = CreateUserRequest(username="test", email="a@b.com", password="123")
    hash_method = lambda _: "hashed_password"
    hashed_request = request.with_hashed_password(hash_method)
    assert hashed_request.password == "hashed_password"
