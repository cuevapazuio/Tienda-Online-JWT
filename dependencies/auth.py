from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from core.security import decodificar_token
from db.database import get_session
from models.usuario import Usuario
from services.auth_service import buscar_por_username


bearer = HTTPBearer(
    auto_error=False
)


SessionDep = Annotated[
    Session,
    Depends(get_session)
]


CredencialesDep = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(bearer)
]


def usuario_actual(
    credenciales: CredencialesDep,
    session: SessionDep
) -> Usuario:

    if credenciales is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticacion requerida"
        )

    try:
        datos = decodificar_token(
            credenciales.credentials
        )

        username = datos.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalido"
            )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado"
        )

    usuario = buscar_por_username(
        username,
        session
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    return usuario