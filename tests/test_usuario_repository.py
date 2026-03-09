
from app.models.usuario import Usuario
from app.repositories import usuario as usuario_repo

def test_add_usuario(session):
    nuevo_usuario = Usuario(nombre="Ana", username="ana123")
    resultado = usuario_repo.add(session, nuevo_usuario)

    assert resultado.id is not None
    assert resultado.nombre == "Ana"
    assert resultado.username == "ana123"

def test_get_usuario(session):
    usuario = Usuario(nombre="Luis", username="luis123")
    session.add(usuario)
    session.commit()

    resultado = usuario_repo.get(session, usuario.id)

    assert resultado is not None
    assert resultado.id == usuario.id


def test_list_all_usuarios(session):
    usuario1 = Usuario(nombre="Ana", username="ana123")
    usuario2 = Usuario(nombre="Luis", username="luis123")
    session.add(usuario1)
    session.add(usuario2)
    session.commit()

    resultado = usuario_repo.list_all(session)

    assert len(resultado) == 2
    assert resultado[0].nombre == "Ana"
    assert resultado[1].nombre == "Luis"
