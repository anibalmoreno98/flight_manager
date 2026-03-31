def test_crear_piloto_guarda_en_bd(session):
    service = PilotoService(session)

    piloto_data = Piloto(
        nombre="Juan",
        apellido="Pérez",
        licencia="ABC123"
    )

    piloto_creado = service.create_piloto_service(piloto_data)

    assert piloto_creado.id is not None

    piloto_db = session.get(Piloto, piloto_creado.id)
    assert piloto_db is not None
    assert piloto_db.licencia == "ABC123"

def test_get_piloto_por_id(session):
    piloto = Piloto(nombre="Ana", apellido="López", licencia="LIC001")
    session.add(piloto)
    session.commit()
    session.refresh(piloto)

    service = PilotoService(session)

    piloto_db = service.get_piloto_service(piloto.id)

    assert piloto_db.id == piloto.id
    assert piloto_db.nombre == "Ana"

def test_listar_pilotos(session):
    session.add(Piloto(nombre="A", apellido="B", licencia="L1"))
    session.add(Piloto(nombre="C", apellido="D", licencia="L2"))
    session.commit()

    service = PilotoService(session)

    pilotos = service.list_pilotos_service()

    assert len(pilotos) == 2

def test_actualizar_piloto(session):
    piloto = Piloto(nombre="Old", apellido="Name", licencia="LIC999")
    session.add(piloto)
    session.commit()
    session.refresh(piloto)

    service = PilotoService(session)

    data = Piloto(nombre="New", apellido="Updated", licencia="LIC999")

    piloto_actualizado = service.update_piloto_service(piloto.id, data)

    assert piloto_actualizado.nombre == "New"
    assert piloto_actualizado.apellido == "Updated"

def test_no_permite_eliminar_piloto_con_misiones(session):
    piloto = Piloto(nombre="Carlos", apellido="Test", licencia="LIC123")
    session.add(piloto)
    session.commit()
    session.refresh(piloto)

    mision = Mision(
        nombre="Misión Test",
        descripcion="Test",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(hours=1),
        creado_por=1,
        estado=EstadoMision.PLANIFICADA,
        piloto_id=piloto.id
    )
    session.add(mision)
    session.commit()

    service = PilotoService(session)

    with pytest.raises(Exception):
        service.delete_piloto_service(piloto.id)

def test_no_permite_eliminar_piloto_con_vuelos(session):
    piloto = Piloto(nombre="Luis", apellido="Vuelo", licencia="LIC777")
    session.add(piloto)
    session.commit()
    session.refresh(piloto)

    vuelo = Vuelo(
        origen="A",
        destino="B",
        fecha=datetime.now(),
        piloto_id=piloto.id
    )
    session.add(vuelo)
    session.commit()

    service = PilotoService(session)

    with pytest.raises(Exception):
        service.delete_piloto_service(piloto.id)

def test_no_permite_asignar_piloto_ocupado(session):
    piloto = Piloto(nombre="Mario", apellido="Ocupado", licencia="LIC888")
    session.add(piloto)
    session.commit()
    session.refresh(piloto)

    # Misión activa
    mision = Mision(
        nombre="Activa",
        descripcion="Test",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(hours=1),
        creado_por=1,
        estado=EstadoMision.EN_CURSO,
        piloto_id=piloto.id
    )
    session.add(mision)
    session.commit()

    service = PilotoService(session)

    with pytest.raises(Exception):
        service._validar_piloto_disponible(piloto.id)

