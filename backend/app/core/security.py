import secrets
from datetime import UTC, datetime, timedelta

import pyotp
import qrcode
import qrcode.image.svg
from jwt import decode, encode
from pwdlib import PasswordHash

from app.core.config import settings

_password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return _password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return _password_hash.verify(password, hashed)


def create_token(sub: str, email: str, roles: list[str], expires_delta: timedelta | None = None) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": sub,
        "email": email,
        "roles": roles,
        "iat": now,
        "exp": now + (expires_delta or timedelta(minutes=settings.jwt_expiration_minutes)),
    }
    return encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    return decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])


def generate_totp_secret() -> str:
    return pyotp.random_base32()


def get_totp_uri(secret: str, email: str) -> str:
    return pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name=settings.app_name)


def generate_qrcode(uri: str) -> str:
    img = qrcode.make(uri, image_factory=qrcode.image.svg.SvgPathImage)
    return img.to_string().decode()


def verify_totp(secret: str, token: str) -> bool:
    return pyotp.TOTP(secret).verify(token)


def generate_safe_filename() -> str:
    return secrets.token_urlsafe(32)
