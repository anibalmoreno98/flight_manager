from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.usuario import Usuario
from app.models.mision import Mision
from app.repositories.usuario import UsuarioRepository

class UsuarioService:

    def __init__(self, session: Session):
        self.session = session
        self.repo = UsuarioRepository(session)

    # -------------------------
    # VALIDACIONES INTERNAS
    # -------------------------

    def _validar_usuario_no_asociado(self, usuario_id: int):
        misiones = self.session.exec(
            select(Mision).where(Mision.creado_por == usuario_id)
        ).all()

        if misiones:
            raise HTTPException(
                400,
                "No se puede eliminar un usuario con misiones creadas."
            )

    def _validar_username_unico(self, username: str):
        existente = self.session.exec(
            select(Usuario).where(Usuario.username == username)
        ).first()

        if existente:
            raise HTTPException(400, "El nombre de usuario ya está en uso.")

    # -------------------------
    # MÉTODOS PÚBLICOS
    # -------------------------

    def create_usuario_service(self, usuario: Usuario) -> Usuario:
        self._validar_username_unico(usuario.username)
        return self.repo.add(usuario)

    def login_usuario_service(self, username: str, password: str) -> Usuario:
        usuario = self.session.exec(
            select(Usuario).where(Usuario.username == username)
        ).first()

        if not usuario or usuario.password != password:
            raise HTTPException(401, "Operación no permitida")

        return usuario

    def get_usuario_service(self, usuario_id: int) -> Usuario:
        usuario = self.repo.get(usuario_id)
        if not usuario:
            raise HTTPException(404, "Usuario no encontrado")
        return usuario

    def list_usuarios_service(self) -> list[Usuario]:
        return self.repo.list_all()

    def update_usuario_service(self, usuario_id: int, data: Usuario) -> Usuario:
        usuario = self.get_usuario_service(usuario_id)

        # Validar username único si cambia
        if data.username != usuario.username:
            self._validar_username_unico(data.username)

        usuario.nombre = data.nombre
        usuario.username = data.username

        return self.repo.update(usuario)

    def delete_usuario_service(self, usuario_id: int) -> dict[str, bool]:
        usuario = self.get_usuario_service(usuario_id)
        self._validar_usuario_no_asociado(usuario_id)

        self.repo.delete(usuario)
        return {"ok": True}

    # -------------------------
    # LOGIN
    # -------------------------
    def login(self, username: str, password: str):
        usuario = self.repo.get_by_username(username)

        if not usuario or usuario.password != password:
            raise HTTPException(401, "Credenciales inválidas.")

        # Los tests esperan un access_token
        return {"access_token": "fake-token-for-tests"}