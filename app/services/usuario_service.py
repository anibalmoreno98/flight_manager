from sqlmodel import Session
from fastapi import HTTPException

from app.models.usuario import Usuario
from app.repositories import usuario as usuario_repo


def create_usuario_service(usuario: Usuario, session: Session):
    return usuario_repo.add(session, usuario)


def get_usuario_service(usuario_id: int, session: Session):
    usuario = usuario_repo.get(session, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


def list_usuarios_service(session: Session):
    return usuario_repo.list_all(session)


def update_usuario_service(usuario_id: int, usuario_data: Usuario, session: Session):
    usuario = usuario_repo.get(session, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre = usuario_data.nombre
    usuario.username = usuario_data.username

    return usuario_repo.update(session, usuario)


def delete_usuario_service(usuario_id: int, session: Session):
    usuario = usuario_repo.get(session, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario_repo.delete(session, usuario)
    return {"ok": True}
