from sqlmodel import Session, select

from models.producto import Producto
from schemas.producto import ProductoCreate


def crear_producto(
    data: ProductoCreate,
    session: Session
):
    producto = Producto(
        nombre=data.nombre,
        descripcion=data.descripcion,
        precio=data.precio,
        stock=data.stock
    )

    session.add(producto)
    session.commit()
    session.refresh(producto)

    return producto


def listar_productos(
    session: Session
):
    consulta = select(Producto)

    return session.exec(consulta).all()


def buscar_producto(
    id_producto: int,
    session: Session
):
    return session.get(
        Producto,
        id_producto
    )


def actualizar_producto(
    producto: Producto,
    data: ProductoCreate,
    session: Session
):
    producto.nombre = data.nombre
    producto.descripcion = data.descripcion
    producto.precio = data.precio
    producto.stock = data.stock

    session.add(producto)
    session.commit()
    session.refresh(producto)

    return producto


def eliminar_producto(
    producto: Producto,
    session: Session
):
    session.delete(producto)
    session.commit()