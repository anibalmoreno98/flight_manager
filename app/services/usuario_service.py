from sqlmodel import Session
from fastapi import HTTPException

from app.models.usuario import Usuario
from app.repositories import usuario as usuario_repo



def create_usuario_service(usuario: Usuario, session: Session, repo=usuario_repo):
    repo_instance = repo.UsuarioRepository(session)
    return repo_instance.add(usuario)


def get_usuario_service(usuario_id: int, session: Session, repo=usuario_repo):
    repo_instance = repo.UsuarioRepository(session)
    usuario = repo_instance.get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


def list_usuarios_service(session: Session, repo=usuario_repo):
    repo_instance = repo.UsuarioRepository(session)
    return repo_instance.list_all()


def update_usuario_service(usuario_id: int, usuario_data: Usuario, session: Session, repo=usuario_repo):
    repo_instance = repo.UsuarioRepository(session)
    usuario = repo_instance.get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre = usuario_data.nombre
    usuario.username = usuario_data.username

    return repo_instance.update(usuario)


def delete_usuario_service(usuario_id: int, session: Session, repo=usuario_repo):
    repo_instance = repo.UsuarioRepository(session)
    usuario = repo_instance.get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    repo_instance.delete(usuario)
    return {"ok": True}
