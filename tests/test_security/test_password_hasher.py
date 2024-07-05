from fast_api_tutorial.security import PwdLibHasher


def test_pwdlib_hasher_hashes_password():
    password = "123"
    hashed = PwdLibHasher().hash_password(password)
    assert hashed != password


def test_pwdlib_hasher_verifies_password():
    password = "123"
    hasher = PwdLibHasher()
    hashed = hasher.hash_password(password)
    assert hasher.verify_password(password, hashed)
    assert not hasher.verify_password("wrong", hashed)
