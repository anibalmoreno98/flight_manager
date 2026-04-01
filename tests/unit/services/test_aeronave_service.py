from datetime import datetime, timedelta

import pytest

from app.models.aeronave import Aeronave
from app.models.estado_mision import EstadoMision
from app.models.mision import Mision
from app.models.vuelo import Vuelo
from app.services.aeronave_service import AeronaveService


def test_crear_aeronave_guarda_en_bd(session):
    service = AeronaveService(session)

    aeronave_data = Aeronave(
        fabricante="Boeing",
        modelo="737",
        numero_serie="SN123",
        velocidad_maxima=850,
        en_mantenimiento=False
    )

    aeronave_creada = service.create_aeronave_service(aeronave_data)

    assert aeronave_creada.id is not None

    aeronave_db = session.get(Aeronave, aeronave_creada.id)
    assert aeronave_db is not None
    assert aeronave_db.modelo == "737"


def test_get_aeronave_por_id(session):
    aeronave = Aeronave(
        fabricante="Airbus",
        modelo="A320",
        numero_serie="SN999",
        velocidad_maxima=830,
        en_mantenimiento=False
    )
    session.add(aeronave)
    session.commit()
    session.refresh(aeronave)

    service = AeronaveService(session)

    aeronave_db = service.get_aeronave_service(aeronave.id)

    assert aeronave_db.id == aeronave.id
    assert aeronave_db.fabricante == "Airbus"


def test_listar_aeronaves(session):
    session.add(Aeronave(fabricante="A", modelo="M1", numero_serie="S1", velocidad_maxima=700))
    session.add(Aeronave(fabricante="B", modelo="M2", numero_serie="S2", velocidad_maxima=750))
    session.commit()

    service = AeronaveService(session)

    aeronaves = service.list_aeronaves_service()

    assert len(aeronaves) == 2


def test_actualizar_aeronave(session):
    aeronave = Aeronave(
        fabricante="Old",
        modelo="Model",
        numero_serie="SN001",
        velocidad_maxima=700,
        en_mantenimiento=False
    )
    session.add(aeronave)
    session.commit()
    session.refresh(aeronave)

    service = AeronaveService(session)

    data = Aeronave(
        fabricante="New",
        modelo="Updated",
        numero_serie="SN001",
        velocidad_maxima=720,
        en_mantenimiento=True
    )

    aeronave_actualizada = service.update_aeronave_service(aeronave.id, data)

    assert aeronave_actualizada.fabricante == "New"
    assert aeronave_actualizada.en_mantenimiento is True


def test_no_permite_eliminar_aeronave_con_misiones(session):
    aeronave = Aeronave(
        fabricante="Test",
        modelo="X",
        numero_serie="SN777",
        velocidad_maxima=800
    )
    session.add(aeronave)
    session.commit()
    session.refresh(aeronave)

    mision = Mision(
        nombre="Misión Test",
        descripcion="Test",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(hours=1),
        creado_por=1,
        estado=EstadoMision.PLANIFICADA,
        aeronave_id=aeronave.id
    )
    session.add(mision)
    session.commit()

    service = AeronaveService(session)

    with pytest.raises(Exception):
        service.delete_aeronave_service(aeronave.id)


def test_no_permite_eliminar_aeronave_con_vuelos(session):
    aeronave = Aeronave(
        fabricante="Test",
        modelo="Y",
        numero_serie="SN888",
        velocidad_maxima=820
    )
    session.add(aeronave)
    session.commit()
    session.refresh(aeronave)

    vuelo = Vuelo(
        nombre="Vuelo Test",
        origen="A",
        destino="B",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(hours=1),
        aeronave_id=aeronave.id,
        piloto_id=1,
        mision_id=1
    )
    session.add(vuelo)
    session.commit()

    service = AeronaveService(session)

    with pytest.raises(Exception):
        service.delete_aeronave_service(aeronave.id)
