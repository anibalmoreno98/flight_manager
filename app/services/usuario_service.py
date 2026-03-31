from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.usuario import Usuario
from app.models.mision import Mision
from app.repositories.usuario import UsuarioRepository

class UsuarioService:

    def __init__(self, session: Session):
        self.session = session
        self.repo = UsuarioRepository(session)

    def _validar_usuario_no_asociado(self, usuario_id: int):
        misiones = self.session.exec(
            select(Mision).where(Mision.creado_por == usuario_id)
        ).all()

        if misiones:
            raise HTTPException(
                400,
                "No se puede eliminar un usuario con misiones creadas."
            )

    def create_usuario_service(self, usuario: Usuario) -> Usuario:
        return self.repo.add(usuario)

    def get_usuario_service(self, usuario_id: int) -> Usuario:
        usuario = self.repo.get(usuario_id)
        if not usuario:
            raise HTTPException(404, "Usuario no encontrado")
        return usuario

    def list_usuarios_service(self) -> list[Usuario]:
        return self.repo.list_all()

    def update_usuario_service(self, usuario_id: int, data: Usuario) -> Usuario:
        usuario = self.get_usuario_service(usuario_id)

        usuario.nombre = data.nombre
        usuario.username = data.username

        return self.repo.update(usuario)

    def delete_usuario_service(self, usuario_id: int) -> dict[str, bool]:
        usuario = self.get_usuario_service(usuario_id)
        self._validar_usuario_no_asociado(usuario_id)

        self.repo.delete(usuario)
        return {"ok": True}

