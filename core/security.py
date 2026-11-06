from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verificar_password(
    password: str,
    password_guardado: str
) -> bool:
    return password_hash.verify(
        password,
        password_guardado
    )


def crear_token(username: str) -> str:
    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    datos = {
        "sub": username,
        "exp": expiracion
    }

    return jwt.encode(
        datos,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decodificar_token(token: str):
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )