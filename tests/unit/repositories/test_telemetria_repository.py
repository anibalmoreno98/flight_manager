from datetime import datetime, timedelta

from app.models.telemetria import Telemetria
from app.repositories.telemetria import TelemetriaRepository


def test_telemetria_repository_add(session):
    repo = TelemetriaRepository(session)

    tele = Telemetria(
        vuelo_id=1,
        latitud=10,
        longitud=20,
        altitud=100,
        velocidad=50,
        altura_maxima=100,
        velocidad_maxima=50,
        timestamp=datetime.now()
    )

    creada = repo.add(tele)
    assert creada.id is not None


def test_telemetria_repository_get(session):
    tele = Telemetria(
        vuelo_id=1,
        latitud=10,
        longitud=20,
        altitud=100,
        velocidad=50,
        altura_maxima=100,
        velocidad_maxima=50,
        timestamp=datetime.now()
    )
    session.add(tele)
    session.commit()
    session.refresh(tele)

    repo = TelemetriaRepository(session)
    obtenida = repo.get(tele.id)

    assert obtenida.id == tele.id


def test_telemetria_repository_list(session):
    session.add(Telemetria(vuelo_id=1, latitud=1, longitud=1, altitud=1, velocidad=1, altura_maxima=100, velocidad_maxima=50, timestamp=datetime.now()))
    session.add(Telemetria(vuelo_id=1, latitud=2, longitud=2, altitud=2, velocidad=2, altura_maxima=100, velocidad_maxima=50, timestamp=datetime.now()))
    session.commit()

    repo = TelemetriaRepository(session)
    lista = repo.list_all()

    assert len(lista) == 2


def test_telemetria_repository_update(session):
    tele = Telemetria(
        vuelo_id=1,
        latitud=10,
        longitud=20,
        altitud=100,
        velocidad=50,
        altura_maxima=100,
        velocidad_maxima=50,
        timestamp=datetime.now()
    )
    session.add(tele)
    session.commit()
    session.refresh(tele)

    repo = TelemetriaRepository(session)
    tele.altitud = 200
    actualizada = repo.update(tele)

    assert actualizada.altitud == 200


def test_telemetria_repository_delete(session):
    tele = Telemetria(
        vuelo_id=1,
        latitud=10,
        longitud=20,
        altitud=100,
        velocidad=50,
        altura_maxima=100,
        velocidad_maxima=50,
        timestamp=datetime.now()
    )
    session.add(tele)
    session.commit()
    session.refresh(tele)

    repo = TelemetriaRepository(session)
    repo.delete(tele)

    assert session.get(Telemetria, tele.id) is None
