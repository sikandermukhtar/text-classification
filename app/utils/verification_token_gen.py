import secrets

def generate_secret_token() -> str:
    return secrets.token_urlsafe(32)
