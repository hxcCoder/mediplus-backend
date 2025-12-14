from utils.security import hash_password, check_password


def test_hash_and_check():
    pwd = "secreto123"
    h = hash_password(pwd)
    assert isinstance(h, (bytes,))
    assert check_password(pwd, h)
    assert not check_password("otro", h)
