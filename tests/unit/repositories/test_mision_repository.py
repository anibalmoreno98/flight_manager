from datetime import datetime, timedelta

from app.models.estado_mision import EstadoMision
from app.models.mision import Mision
from app.repositories.mision import MisionRepository


def test_mision_repository_add(session):
    repo = MisionRepository(session)

    mision = Mision(
        nombre="Test",
        descripcion="Desc",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now(),
        creado_por=1,
        estado=EstadoMision.CREADA
    )

    creada = repo.add(mision)
    assert creada.id is not None


def test_mision_repository_get(session):
    mision = Mision(
        nombre="Test",
        descripcion="Desc",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now(),
        creado_por=1,
        estado=EstadoMision.CREADA
    )
    session.add(mision)
    session.commit()
    session.refresh(mision)

    repo = MisionRepository(session)
    obtenida = repo.get(mision.id)

    assert obtenida.id == mision.id


def test_mision_repository_list(session):
    session.add(Mision(nombre="A", descripcion="X", fecha_inicio=datetime.now(), fecha_fin=datetime.now(), creado_por=1, estado=EstadoMision.CREADA))
    session.add(Mision(nombre="B", descripcion="Y", fecha_inicio=datetime.now(), fecha_fin=datetime.now(), creado_por=1, estado=EstadoMision.CREADA))
    session.commit()

    repo = MisionRepository(session)
    lista = repo.list_all()

    assert len(lista) == 2


def test_mision_repository_update(session):
    mision = Mision(
        nombre="Old",
        descripcion="Desc",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now(),
        creado_por=1,
        estado=EstadoMision.CREADA
    )
    session.add(mision)
    session.commit()
    session.refresh(mision)

    repo = MisionRepository(session)
    mision.nombre = "New"
    actualizada = repo.update(mision)

    assert actualizada.nombre == "New"


def test_mision_repository_delete(session):
    mision = Mision(
        nombre="Delete",
        descripcion="Desc",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now(),
        creado_por=1,
        estado=EstadoMision.CREADA
    )
    session.add(mision)
    session.commit()
    session.refresh(mision)

    repo = MisionRepository(session)
    repo.delete(mision)

    assert session.get(Mision, mision.id) is None
