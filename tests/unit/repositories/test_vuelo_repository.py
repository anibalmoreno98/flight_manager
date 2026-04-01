from datetime import datetime, timedelta

from app.models.vuelo import Vuelo
from app.repositories.vuelo import VueloRepository


def test_vuelo_repository_add(session):
    repo = VueloRepository(session)

    vuelo = Vuelo(
        nombre="Vuelo Test",
        origen="A",
        destino="B",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(hours=1),
        piloto_id=1,
        aeronave_id=1,
        mision_id=1
    )

    creado = repo.add(vuelo)
    assert creado.id is not None


def test_vuelo_repository_get(session):
    vuelo = Vuelo(
        nombre="Vuelo Test",
        origen="A",
        destino="B",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(hours=1),
        piloto_id=1,
        aeronave_id=1,
        mision_id=1
    )
    session.add(vuelo)
    session.commit()
    session.refresh(vuelo)

    repo = VueloRepository(session)
    obtenido = repo.get(vuelo.id)

    assert obtenido.id == vuelo.id


def test_vuelo_repository_list(session):
    session.add(Vuelo(
        nombre="Vuelo Test",
        origen="A",
        destino="B",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(hours=1),
        piloto_id=1,
        aeronave_id=1,
        mision_id=1
    ))
    session.add(Vuelo(
        nombre="Vuelo Test 2",
        origen="C",
        destino="D",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(hours=1),
        piloto_id=1,
        aeronave_id=1,
        mision_id=1
    ))
    session.commit()

    repo = VueloRepository(session)
    lista = repo.list_all()

    assert len(lista) == 2


def test_vuelo_repository_update(session):
    vuelo = Vuelo(
        nombre="Vuelo Test",
        origen="A",
        destino="B",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(hours=1),
        piloto_id=1,
        aeronave_id=1,
        mision_id=1
    )
    session.add(vuelo)
    session.commit()
    session.refresh(vuelo)

    repo = VueloRepository(session)
    vuelo.destino = "Z"
    actualizado = repo.update(vuelo)

    assert actualizado.destino == "Z"


def test_vuelo_repository_delete(session):
    vuelo = Vuelo(
        nombre="Vuelo Test",
        origen="A",
        destino="B",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(hours=1),
        piloto_id=1,
        aeronave_id=1,
        mision_id=1
    )
    session.add(vuelo)
    session.commit()
    session.refresh(vuelo)

    repo = VueloRepository(session)
    repo.delete(vuelo)

    assert session.get(Vuelo, vuelo.id) is None
