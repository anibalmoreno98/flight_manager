from sqlmodel import Session
from fastapi import HTTPException

from app.models.usuario import Usuario
from app.repositories.usuario import UsuarioRepository

class UsuarioService:

    def __init__(self, session: Session):
        self.session = session
        self.repo = UsuarioRepository(session)


    def create_usuario_service(self, usuario: Usuario) -> Usuario:
        return self.repo.add(usuario)

    def get_usuario_service(self, usuario_id: int) -> Usuario:
        usuario = self.repo.get(usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario


    def list_usuarios_service(self) -> list[Usuario]:
        return self.repo.list_all()


    def update_usuario_service(self, usuario_id: int, usuario_data: Usuario) -> Usuario:
        usuario = self.repo.get(usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        usuario.nombre = usuario_data.nombre
        usuario.username = usuario_data.username

        return self.repo.update(usuario)


    def update_usuario_service(usuario_id: int, usuario_data: Usuario, session: Session, repo=usuario_repo) -> Usuario:
        usuario = repo.get(session, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        usuario.nombre = usuario_data.nombre
        usuario.username = usuario_data.username

        return repo.update(session, usuario)


    def delete_usuario_service(usuario_id: int, session: Session, repo=usuario_repo) -> dict[str, bool]:
        usuario = repo.get(session, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        repo.delete(session, usuario)
        return {"ok": True}
