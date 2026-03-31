def test_crear_usuario_guarda_en_bd(session):
    service = UsuarioService(session)

    usuario_data = Usuario(
        nombre="Usuario Test",
        username="usuario_test",
        password="1234"
    )

    usuario_creado = service.create_usuario_service(usuario_data)

    assert usuario_creado.id is not None

    usuario_db = session.get(Usuario, usuario_creado.id)
    assert usuario_db is not None
    assert usuario_db.username == "usuario_test"

def test_no_permite_username_duplicado(session):
    service = UsuarioService(session)

    usuario1 = Usuario(nombre="A", username="duplicado", password="1234")
    usuario2 = Usuario(nombre="B", username="duplicado", password="abcd")

    service.create_usuario_service(usuario1)

    with pytest.raises(Exception):
        service.create_usuario_service(usuario2)

def test_login_correcto(session):
    service = UsuarioService(session)

    usuario = Usuario(
        nombre="Login Test",
        username="login_user",
        password="1234"
    )
    session.add(usuario)
    session.commit()

    usuario_login = service.login_usuario_service("login_user", "1234")

    assert usuario_login is not None
    assert usuario_login.username == "login_user"

def test_login_incorrecto_password(session):
    service = UsuarioService(session)

    usuario = Usuario(
        nombre="Login Test",
        username="login_user2",
        password="correcta"
    )
    session.add(usuario)
    session.commit()

    with pytest.raises(Exception):
        service.login_usuario_service("login_user2", "incorrecta")

def test_get_usuario_por_id(session):
    usuario = Usuario(
        nombre="Usuario Test",
        username="usuario_get",
        password="1234"
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    service = UsuarioService(session)

    usuario_db = service.get_usuario_service(usuario.id)

    assert usuario_db.id == usuario.id
    assert usuario_db.username == "usuario_get"

def test_listar_usuarios(session):
    session.add(Usuario(nombre="A", username="u1", password="1"))
    session.add(Usuario(nombre="B", username="u2", password="2"))
    session.commit()

    service = UsuarioService(session)

    usuarios = service.list_usuarios_service()

    assert len(usuarios) == 2

def test_no_permite_eliminar_usuario_con_misiones(session):
    usuario = Usuario(
        nombre="Usuario Test",
        username="usuario_misiones",
        password="1234"
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    mision = Mision(
        nombre="Misión Test",
        descripcion="Test",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(hours=1),
        creado_por=usuario.id,
        estado=EstadoMision.PLANIFICADA
    )
    session.add(mision)
    session.commit()

    service = UsuarioService(session)

    with pytest.raises(Exception):
        service.delete_usuario_service(usuario.id)

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
            raise HTTPException(401, "Credenciales inválidas.")

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
