from passlib.hash import sha512_crypt as crypto


def hash_password(password: str):
    hashed_password = crypto.hash(password, rounds=100_000)
    return hashed_password


def verify_password(password: str, hashed_password: str):
    return crypto.verify(password, hashed_password)
