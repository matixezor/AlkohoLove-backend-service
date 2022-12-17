import hashlib


def dehash_token(token: str):
    hashed_code = hashlib.sha256()
    hashed_code.update(bytes.fromhex(token))
    changed_code = hashed_code.hexdigest()
    return changed_code


def hash_token(token: bytes):
    hashed_code = hashlib.sha256()
    hashed_code.update(token)
    code = hashed_code.hexdigest()
    return code
