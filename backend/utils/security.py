from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


# Password hashing context - using argon2 as primary, bcrypt as fallback
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for the provided password.
    Truncate password if it exceeds bcrypt's 72-byte limit.
    """
    # Bcrypt has a 72-byte password limit, so we truncate if necessary
    truncated_password = password[:72]
    return pwd_context.hash(truncated_password)