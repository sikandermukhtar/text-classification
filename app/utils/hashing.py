from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt", "argon2"],
    default="argon2",
    deprecated=["bcrypt"]
)


def hash(plain: str) -> str:
    if not plain:
        raise ValueError("You cannot hash empty string")
    return pwd_context.hash(plain)


def verify_hash(plain: str, hashed: str) -> bool:
    if not plain:
        raise ValueError("Provide valid plain string")
    if not hashed:
        raise ValueError("Provide valid hashed string")

    return pwd_context.verify(plain, hashed)

def needs_rehash(hashed: str) -> bool:
    return pwd_context.needs_update(hashed)