import bcrypt
import hmac


# Hash a password
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


# Verify a password
def check_password(password: str, hashed_password: str) -> bool:
    return hmac.compare_digest(
        bcrypt.hashpw(password.encode(), hashed_password.encode()),
        hashed_password.encode()
    )
