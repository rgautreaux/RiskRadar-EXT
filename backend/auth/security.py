from __future__ import annotations

import base64
import hashlib
import hmac
from functools import lru_cache

from cryptography.fernet import Fernet, InvalidToken
from passlib.context import CryptContext

from config.settings import settings

_pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def normalize_email(email: str) -> str:
    return email.strip().lower()


def _secret_material() -> str:
    return (settings.EMAIL_ENCRYPTION_KEY or settings.JWT_SECRET_KEY).strip()


@lru_cache(maxsize=1)
def _fernet() -> Fernet:
    key_material = _secret_material()
    try:
        return Fernet(key_material.encode("utf-8"))
    except Exception:
        digest = hashlib.sha256(key_material.encode("utf-8")).digest()
        return Fernet(base64.urlsafe_b64encode(digest))


def _lookup_key() -> bytes:
    key_material = (settings.EMAIL_HASH_SECRET or settings.EMAIL_ENCRYPTION_KEY or settings.JWT_SECRET_KEY).strip()
    return hashlib.sha256(key_material.encode("utf-8")).digest()


def encrypt_email(email: str) -> str:
    normalized_email = normalize_email(email)
    return _fernet().encrypt(normalized_email.encode("utf-8")).decode("utf-8")


def decrypt_email(token: str) -> str:
    return _fernet().decrypt(token.encode("utf-8")).decode("utf-8")


def is_encrypted_email(value: str) -> bool:
    try:
        decrypt_email(value)
    except (InvalidToken, ValueError, TypeError, AttributeError):
        return False
    return True


def hash_email(email: str) -> str:
    normalized_email = normalize_email(email)
    digest = hmac.new(_lookup_key(), normalized_email.encode("utf-8"), hashlib.sha256)
    return digest.hexdigest()


def password_hash(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return _pwd_context.verify(password, hashed_password)


def validate_password_strength(password: str) -> tuple[bool, str]:
    minimum_length = settings.PASSWORD_MIN_LENGTH
    if len(password) < minimum_length:
        return False, f"Password must be at least {minimum_length} characters long"
    if not any(character.islower() for character in password):
        return False, "Password must include a lowercase letter"
    if not any(character.isupper() for character in password):
        return False, "Password must include an uppercase letter"
    if not any(character.isdigit() for character in password):
        return False, "Password must include a number"
    if not any(not character.isalnum() for character in password):
        return False, "Password must include a special character"
    return True, ""
