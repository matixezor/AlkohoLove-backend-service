import hashlib


async def hash_token(token: str):
    hashed_code = hashlib.sha256()
    hashed_code.update(bytes.fromhex(token))
    change_password_code = hashed_code.hexdigest()
    return change_password_code