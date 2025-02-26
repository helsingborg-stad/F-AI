from passlib.context import CryptContext


def hash_secret(secret: str) -> str:
    crypt_context = CryptContext(schemes=['argon2'], deprecated='auto')
    return crypt_context.hash(secret)


def verify_hash(expected: str, hashed_value: str) -> bool:
    crypt_context = CryptContext(schemes=['argon2'], deprecated='auto')
    return crypt_context.verify(expected, hashed_value)
