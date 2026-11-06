from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from db.database import get_session
from schemas.usuario import (
    UsuarioCreate,
    UsuarioLogin,
    UsuarioRead,
    Token,
)
from services.auth_service import (
    registrar_usuario,
    autenticar_usuario,
    buscar_por_username,
    buscar_por_email,
)
from core.security import crear_token


router = APIRouter(
    prefix="/auth",
    tags=["Autenticacion"]
)


SessionDep = Annotated[
    Session,
    Depends(get_session)
]


@router.post(
    "/register",
    response_model=UsuarioRead,
    status_code=status.HTTP_201_CREATED
)
def register(
    data: UsuarioCreate,
    session: SessionDep
):
    if buscar_por_username(data.username, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El username ya existe"
        )

    if buscar_por_email(data.email, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya existe"
        )

    return registrar_usuario(
        data,
        session
    )


@router.post(
    "/login",
    response_model=Token
)
def login(
    data: UsuarioLogin,
    session: SessionDep
):
    usuario = autenticar_usuario(
        data.username,
        data.password,
        session
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )

    token = crear_token(
        usuario.username
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }