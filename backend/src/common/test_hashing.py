from src.common.hashing import hash_secret, verify_hash


def test_hash_verify():
    value = 'my secret value'
    hashed = hash_secret(value)
    result = verify_hash(value, hashed)

    assert len(hashed) > 0
    assert result
