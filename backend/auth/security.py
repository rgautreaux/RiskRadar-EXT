from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from functools import lru_cache

from cryptography.fernet import Fernet, InvalidToken
from passlib.context import CryptContext

from backend.config.settings import settings

_pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
SESSION_COOKIE_NAME = "riskradar_session"


def normalize_email(email: str) -> str:
    return email.strip().lower()


def _secret_material() -> str:
    return (settings.EMAIL_ENCRYPTION_KEY or settings.JWT_SECRET_KEY).strip()


@lru_cache(maxsize=1)
def _fernet() -> Fernet:
    key_material = _secret_material()
    try:
        return Fernet(key_material.encode("utf-8"))
    except (ValueError, TypeError, binascii.Error):
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


def _session_secret() -> bytes:
    key_material = (settings.JWT_SECRET_KEY or settings.EMAIL_HASH_SECRET or settings.EMAIL_ENCRYPTION_KEY).strip()
    return hashlib.sha256(key_material.encode("utf-8")).digest()


def _base64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("utf-8").rstrip("=")


def _base64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("utf-8"))


def create_session_token(user_id: int) -> tuple[str, datetime]:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "exp": int(expires_at.timestamp()),
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "sub": int(user_id),
    }
    payload_text = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    payload_part = _base64url_encode(payload_text)
    signature = hmac.new(_session_secret(), payload_part.encode("utf-8"), hashlib.sha256).digest()
    return f"{payload_part}.{_base64url_encode(signature)}", expires_at


def verify_session_token(token: str) -> int | None:
    try:
        payload_part, signature_part = token.split(".", 1)
        expected_signature = hmac.new(_session_secret(), payload_part.encode("utf-8"), hashlib.sha256).digest()
        provided_signature = _base64url_decode(signature_part)
        if not hmac.compare_digest(expected_signature, provided_signature):
            return None

        payload = json.loads(_base64url_decode(payload_part).decode("utf-8"))
        if not isinstance(payload, dict):
            return None

        expires_at = int(payload.get("exp", 0))
        subject = int(payload.get("sub", 0))
        if subject < 1:
            return None
        if expires_at <= int(datetime.now(timezone.utc).timestamp()):
            return None
        return subject
    except (ValueError, TypeError, json.JSONDecodeError, UnicodeDecodeError, binascii.Error):
        return None
