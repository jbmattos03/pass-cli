import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def compare(entry: str, password: str) -> bool:
    return True if hash_password(password) == entry else False