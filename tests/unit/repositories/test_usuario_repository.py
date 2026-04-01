

from app.models.usuario import Usuario
from app.repositories.usuario import UsuarioRepository


def test_usuario_repository_add(session):
    repo = UsuarioRepository(session)

    usuario = Usuario(nombre="Test", username="u1", password="1234")
    creado = repo.add(usuario)

    assert creado.id is not None
    assert session.get(Usuario, creado.id) is not None


def test_usuario_repository_get(session):
    usuario = Usuario(nombre="Test", username="u2", password="1234")
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    repo = UsuarioRepository(session)
    obtenido = repo.get(usuario.id)

    assert obtenido.id == usuario.id


def test_usuario_repository_list(session):
    session.add(Usuario(nombre="A", username="u3", password="1"))
    session.add(Usuario(nombre="B", username="u4", password="2"))
    session.commit()

    repo = UsuarioRepository(session)
    lista = repo.list_all()

    assert len(lista) == 2


def test_usuario_repository_update(session):
    usuario = Usuario(nombre="Old", username="u5", password="123")
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    repo = UsuarioRepository(session)
    usuario.nombre = "New"
    actualizado = repo.update(usuario)

    assert actualizado.nombre == "New"


def test_usuario_repository_delete(session):
    usuario = Usuario(nombre="Delete", username="u6", password="123")
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    repo = UsuarioRepository(session)
    repo.delete(usuario)

    assert session.get(Usuario, usuario.id) is None

