

from app.models.piloto import Piloto
from app.repositories.piloto import PilotoRepository


def test_piloto_repository_add(session):
    repo = PilotoRepository(session)

    piloto = Piloto(nombre="Juan", apellido="Pérez", licencia="LIC001")
    creado = repo.add(piloto)

    assert creado.id is not None


def test_piloto_repository_get(session):
    piloto = Piloto(nombre="Ana", apellido="López", licencia="LIC002")
    session.add(piloto)
    session.commit()
    session.refresh(piloto)

    repo = PilotoRepository(session)
    obtenido = repo.get(piloto.id)

    assert obtenido.id == piloto.id


def test_piloto_repository_list(session):
    session.add(Piloto(nombre="A", apellido="B", licencia="L1"))
    session.add(Piloto(nombre="C", apellido="D", licencia="L2"))
    session.commit()

    repo = PilotoRepository(session)
    lista = repo.list_all()

    assert len(lista) == 2


def test_piloto_repository_update(session):
    piloto = Piloto(nombre="Old", apellido="Name", licencia="LIC003")
    session.add(piloto)
    session.commit()
    session.refresh(piloto)

    repo = PilotoRepository(session)
    piloto.nombre = "New"
    actualizado = repo.update(piloto)

    assert actualizado.nombre == "New"


def test_piloto_repository_delete(session):
    piloto = Piloto(nombre="Delete", apellido="X", licencia="LIC004")
    session.add(piloto)
    session.commit()
    session.refresh(piloto)

    repo = PilotoRepository(session)
    repo.delete(piloto)

    assert session.get(Piloto, piloto.id) is None
