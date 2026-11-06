from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from db.database import get_session
from dependencies.auth import usuario_actual
from models.usuario import Usuario
from schemas.producto import ProductoCreate, ProductoRead
from services.producto_service import (
    crear_producto,
    listar_productos,
    buscar_producto,
    actualizar_producto,
    eliminar_producto,
)


router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


SessionDep = Annotated[
    Session,
    Depends(get_session)
]


UsuarioDep = Annotated[
    Usuario,
    Depends(usuario_actual)
]


@router.post(
    "/",
    response_model=ProductoRead,
    status_code=status.HTTP_201_CREATED
)
def crear(
    data: ProductoCreate,
    session: SessionDep,
    usuario: UsuarioDep
):
    return crear_producto(
        data,
        session
    )


@router.get(
    "/",
    response_model=list[ProductoRead]
)
def listar(
    session: SessionDep,
    usuario: UsuarioDep
):
    return listar_productos(
        session
    )


@router.get(
    "/{id_producto}",
    response_model=ProductoRead
)
def obtener(
    id_producto: int,
    session: SessionDep,
    usuario: UsuarioDep
):
    producto = buscar_producto(
        id_producto,
        session
    )

    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return producto


@router.put(
    "/{id_producto}",
    response_model=ProductoRead
)
def actualizar(
    id_producto: int,
    data: ProductoCreate,
    session: SessionDep,
    usuario: UsuarioDep
):
    producto = buscar_producto(
        id_producto,
        session
    )

    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return actualizar_producto(
        producto,
        data,
        session
    )


@router.delete(
    "/{id_producto}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar(
    id_producto: int,
    session: SessionDep,
    usuario: UsuarioDep
):
    producto = buscar_producto(
        id_producto,
        session
    )

    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    eliminar_producto(
        producto,
        session
    )

    return None