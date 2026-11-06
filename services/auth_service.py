from sqlmodel import Session, select

from models.usuario import Usuario
from schemas.usuario import UsuarioCreate
from core.security import hash_password, verificar_password


def buscar_por_username(
    username: str,
    session: Session
):
    consulta = select(Usuario).where(
        Usuario.username == username
    )

    return session.exec(consulta).first()


def buscar_por_email(
    email: str,
    session: Session
):
    consulta = select(Usuario).where(
        Usuario.email == email
    )

    return session.exec(consulta).first()


def registrar_usuario(
    data: UsuarioCreate,
    session: Session
):
    usuario = Usuario(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password)
    )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


def autenticar_usuario(
    username: str,
    password: str,
    session: Session
):
    usuario = buscar_por_username(
        username,
        session
    )

    if usuario is None:
        return None

    if not verificar_password(
        password,
        usuario.password_hash
    ):
        return None

    return usuario