# tests/unit/services/test_mision_service.py

import pytest
from datetime import datetime, timedelta

from app.services.mision_service import MisionService
from app.models.mision import Mision, EstadoMision
from app.models.usuario import Usuario


def test_crear_mision_guarda_en_bd(session):
    # 1. Creamos un usuario que será el creador de la misión
    usuario = Usuario(
        nombre="Usuario Test",
        username="usuario_test",
        password="1234"
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    # 2. Creamos el servicio usando la sesión de tests
    service = MisionService(session)

    # 3. Definimos los datos de la misión a crear
    inicio = datetime.now()
    fin = inicio + timedelta(hours=1)

    mision_data = Mision(
        nombre="Misión 1",
        descripcion="Misión de prueba",
        fecha_inicio=inicio,
        fecha_fin=fin,
        creado_por=usuario.id,
        estado=EstadoMision.PLANIFICADA,
    )

    # 4. Llamamos al service para crear la misión
    mision_creada = service.create_mision_service(mision_data)

    # 5. Afirmamos que la misión se ha creado con un ID
    assert mision_creada.id is not None

    # 6. Leemos la misión desde la BD para asegurarnos de que está guardada
    mision_db = session.get(Mision, mision_creada.id)

    assert mision_db is not None
    assert mision_db.nombre == "Misión 1"
    assert mision_db.descripcion == "Misión de prueba"
    assert mision_db.creado_por == usuario.id
    assert mision_db.estado == EstadoMision.PLANIFICADA
    assert mision_db.fecha_inicio is not None
    assert mision_db.fecha_fin is not None


def test_no_permite_retroceder_estado(session):
    # 1. Creamos un usuario
    usuario = Usuario(
        nombre="Usuario Test",
        username="usuario_test2",
        password="1234"
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    # 2. Creamos una misión en estado EN_CURSO
    inicio = datetime.now()
    fin = inicio + timedelta(hours=1)

    mision = Mision(
        nombre="Misión Estado",
        descripcion="Test de estados",
        fecha_inicio=inicio,
        fecha_fin=fin,
        creado_por=usuario.id,
        estado=EstadoMision.EN_CURSO,
    )
    session.add(mision)
    session.commit()
    session.refresh(mision)

    service = MisionService(session)

    # 3. Intentamos retroceder a PLANIFICADA
    mision_update = Mision(
        nombre="Misión Estado",
        descripcion="Test de estados",
        fecha_inicio=inicio,
        fecha_fin=fin,
        creado_por=usuario.id,
        estado=EstadoMision.PLANIFICADA,  # ← retroceso ilegal
    )

    # 4. Debe lanzar excepción
    with pytest.raises(Exception):
        service.update_mision_service(mision.id, mision_update)


def test_no_permite_iniciar_mision_sin_piloto(session):
    # Crear usuario
    usuario = Usuario(
        nombre="Usuario Test",
        username="usuario_test3",
        password="1234"
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    # Crear misión PLANIFICADA sin piloto
    inicio = datetime.now()
    fin = inicio + timedelta(hours=1)

    mision = Mision(
        nombre="Misión sin piloto",
        descripcion="Test",
        fecha_inicio=inicio,
        fecha_fin=fin,
        creado_por=usuario.id,
        estado=EstadoMision.PLANIFICADA,
        piloto_id=None
    )
    session.add(mision)
    session.commit()
    session.refresh(mision)

    service = MisionService(session)

    # Intentar pasarla a EN_CURSO sin piloto
    mision_update = Mision(
        nombre=mision.nombre,
        descripcion=mision.descripcion,
        fecha_inicio=inicio,
        fecha_fin=fin,
        creado_por=usuario.id,
        estado=EstadoMision.EN_CURSO,
        piloto_id=None
    )

    with pytest.raises(Exception):
        service.update_mision_service(mision.id, mision_update)


def test_no_permite_finalizar_sin_fecha_fin(session):
    # Crear usuario
    usuario = Usuario(
        nombre="Usuario Test",
        username="usuario_test4",
        password="1234"
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    # Crear misión EN_CURSO
    inicio = datetime.now()

    mision = Mision(
        nombre="Misión sin fecha_fin",
        descripcion="Test",
        fecha_inicio=inicio,
        fecha_fin=inicio + timedelta(hours=1),
        creado_por=usuario.id,
        estado=EstadoMision.EN_CURSO,
        piloto_id=1
    )
    session.add(mision)
    session.commit()
    session.refresh(mision)

    service = MisionService(session)

    # Intentar finalizar sin fecha_fin válida
    mision_update = Mision(
        nombre=mision.nombre,
        descripcion=mision.descripcion,
        fecha_inicio=inicio,
        fecha_fin=None,  # ← inválido
        creado_por=usuario.id,
        estado=EstadoMision.FINALIZADA,
        piloto_id=1
    )

    with pytest.raises(Exception):
        service.update_mision_service(mision.id, mision_update)


def test_no_permite_finalizar_si_no_esta_en_curso(session):
    # Crear usuario
    usuario = Usuario(
        nombre="Usuario Test",
        username="usuario_test5",
        password="1234"
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    # Crear misión PLANIFICADA
    inicio = datetime.now()
    fin = inicio + timedelta(hours=1)

    mision = Mision(
        nombre="Misión no en curso",
        descripcion="Test",
        fecha_inicio=inicio,
        fecha_fin=fin,
        creado_por=usuario.id,
        estado=EstadoMision.PLANIFICADA,
        piloto_id=1
    )
    session.add(mision)
    session.commit()
    session.refresh(mision)

    service = MisionService(session)

    # Intentar finalizar estando PLANIFICADA
    mision_update = Mision(
        nombre=mision.nombre,
        descripcion=mision.descripcion,
        fecha_inicio=inicio,
        fecha_fin=fin,
        creado_por=usuario.id,
        estado=EstadoMision.FINALIZADA,
        piloto_id=1
    )

    with pytest.raises(Exception):
        service.update_mision_service(mision.id, mision_update)

def test_no_permite_asignar_piloto_inexistente(session):
    # Crear usuario
    usuario = Usuario(
        nombre="Usuario Test",
        username="usuario_test6",
        password="1234"
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    # Crear misión PLANIFICADA sin piloto
    inicio = datetime.now()
    fin = inicio + timedelta(hours=1)

    mision = Mision(
        nombre="Misión piloto inexistente",
        descripcion="Test",
        fecha_inicio=inicio,
        fecha_fin=fin,
        creado_por=usuario.id,
        estado=EstadoMision.PLANIFICADA,
        piloto_id=None
    )
    session.add(mision)
    session.commit()
    session.refresh(mision)

    service = MisionService(session)

    # Intentar asignar piloto que NO existe
    mision_update = Mision(
        nombre=mision.nombre,
        descripcion=mision.descripcion,
        fecha_inicio=inicio,
        fecha_fin=fin,
        creado_por=usuario.id,
        estado=EstadoMision.PLANIFICADA,
        piloto_id=9999  # ← piloto inexistente
    )

    with pytest.raises(Exception):
        service.update_mision_service(mision.id, mision_update)


def test_no_permite_asignar_aeronave_inexistente(session):
    # Crear usuario
    usuario = Usuario(
        nombre="Usuario Test",
        username="usuario_test7",
        password="1234"
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    # Crear misión PLANIFICADA sin aeronave
    inicio = datetime.now()
    fin = inicio + timedelta(hours=1)

    mision = Mision(
        nombre="Misión aeronave inexistente",
        descripcion="Test",
        fecha_inicio=inicio,
        fecha_fin=fin,
        creado_por=usuario.id,
        estado=EstadoMision.PLANIFICADA,
        aeronave_id=None
    )
    session.add(mision)
    session.commit()
    session.refresh(mision)

    service = MisionService(session)

    # Intentar asignar aeronave que NO existe
    mision_update = Mision(
        nombre=mision.nombre,
        descripcion=mision.descripcion,
        fecha_inicio=inicio,
        fecha_fin=fin,
        creado_por=usuario.id,
        estado=EstadoMision.PLANIFICADA,
        aeronave_id=9999  # ← aeronave inexistente
    )

    with pytest.raises(Exception):
        service.update_mision_service(mision.id, mision_update)


def test_no_permite_finalizar_si_no_esta_en_curso(session):
    # Crear usuario
    usuario = Usuario(
        nombre="Usuario Test",
        username="usuario_test8",
        password="1234"
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    # Crear misión PLANIFICADA
    inicio = datetime.now()
    fin = inicio + timedelta(hours=1)

    mision = Mision(
        nombre="Misión no en curso",
        descripcion="Test",
        fecha_inicio=inicio,
        fecha_fin=fin,
        creado_por=usuario.id,
        estado=EstadoMision.PLANIFICADA,
        piloto_id=1
    )
    session.add(mision)
    session.commit()
    session.refresh(mision)

    service = MisionService(session)

    # Intentar finalizar estando PLANIFICADA
    mision_update = Mision(
        nombre=mision.nombre,
        descripcion=mision.descripcion,
        fecha_inicio=inicio,
        fecha_fin=fin,
        creado_por=usuario.id,
        estado=EstadoMision.FINALIZADA,
        piloto_id=1
    )

    with pytest.raises(Exception):
        service.update_mision_service(mision.id, mision_update)
