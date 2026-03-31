


def test_crear_telemetria_guarda_en_bd(session):
    # Crear vuelo y misión activa
    mision = Mision(
        nombre="Misión",
        descripcion="Test",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(hours=1),
        creado_por=1,
        estado=EstadoMision.EN_CURSO
    )
    session.add(mision)
    session.commit()

    vuelo = Vuelo(
        origen="A",
        destino="B",
        fecha=datetime.now(),
        piloto_id=1,
        aeronave_id=1,
        mision_id=mision.id
    )
    session.add(vuelo)
    session.commit()
    session.refresh(vuelo)

    service = TelemetriaService(session)

    tele_data = Telemetria(
        vuelo_id=vuelo.id,
        latitud=10.0,
        longitud=20.0,
        altitud=100.0,
        velocidad=50.0,
        timestamp=datetime.now()
    )

    tele_creada = service.create_telemetria_service(tele_data)

    assert tele_creada.id is not None
    assert tele_creada.latitud == 10.0

def test_no_permite_crear_telemetria_con_vuelo_inexistente(session):
    service = TelemetriaService(session)

    tele = Telemetria(
        vuelo_id=9999,
        latitud=1.0,
        longitud=2.0,
        altitud=3.0,
        velocidad=4.0,
        timestamp=datetime.now()
    )

    with pytest.raises(Exception):
        service.create_telemetria_service(tele)

def test_no_permite_crear_telemetria_en_mision_finalizada(session):
    mision = Mision(
        nombre="Finalizada",
        descripcion="Test",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now(),
        creado_por=1,
        estado=EstadoMision.FINALIZADA
    )
    session.add(mision)
    session.commit()

    vuelo = Vuelo(
        origen="A",
        destino="B",
        fecha=datetime.now(),
        piloto_id=1,
        aeronave_id=1,
        mision_id=mision.id
    )
    session.add(vuelo)
    session.commit()
    session.refresh(vuelo)

    service = TelemetriaService(session)

    tele = Telemetria(
        vuelo_id=vuelo.id,
        latitud=1.0,
        longitud=2.0,
        altitud=3.0,
        velocidad=4.0,
        timestamp=datetime.now()
    )

    with pytest.raises(Exception):
        service.create_telemetria_service(tele)

def test_get_telemetria_por_id(session):
    tele = Telemetria(
        vuelo_id=1,
        latitud=10,
        longitud=20,
        altitud=100,
        velocidad=50,
        timestamp=datetime.now()
    )
    session.add(tele)
    session.commit()
    session.refresh(tele)

    service = TelemetriaService(session)

    tele_db = service.get_telemetria_service(tele.id)

    assert tele_db.id == tele.id
    assert tele_db.altitud == 100

def test_listar_telemetria(session):
    session.add(Telemetria(vuelo_id=1, latitud=1, longitud=1, altitud=1, velocidad=1, timestamp=datetime.now()))
    session.add(Telemetria(vuelo_id=1, latitud=2, longitud=2, altitud=2, velocidad=2, timestamp=datetime.now()))
    session.commit()

    service = TelemetriaService(session)

    tele = service.list_telemetria_service()

    assert len(tele) == 2

def test_actualizar_telemetria(session):
    # Crear misión activa y vuelo
    mision = Mision(
        nombre="Activa",
        descripcion="Test",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(hours=1),
        creado_por=1,
        estado=EstadoMision.EN_CURSO
    )
    session.add(mision)
    session.commit()

    vuelo = Vuelo(
        origen="A",
        destino="B",
        fecha=datetime.now(),
        piloto_id=1,
        aeronave_id=1,
        mision_id=mision.id
    )
    session.add(vuelo)
    session.commit()
    session.refresh(vuelo)

    tele = Telemetria(
        vuelo_id=vuelo.id,
        latitud=10,
        longitud=20,
        altitud=100,
        velocidad=50,
        timestamp=datetime.now()
    )
    session.add(tele)
    session.commit()
    session.refresh(tele)

    service = TelemetriaService(session)

    data = Telemetria(
        vuelo_id=vuelo.id,
        latitud=10,
        longitud=20,
        altitud=200,
        velocidad=80,
        timestamp=datetime.now()
    )

    tele_actualizada = service.update_telemetria_service(tele.id, data)

    assert tele_actualizada.altitud == 200
    assert tele_actualizada.velocidad == 80

def test_no_permite_actualizar_telemetria_en_mision_finalizada(session):
    mision = Mision(
        nombre="Finalizada",
        descripcion="Test",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now(),
        creado_por=1,
        estado=EstadoMision.FINALIZADA
    )
    session.add(mision)
    session.commit()

    vuelo = Vuelo(
        origen="A",
        destino="B",
        fecha=datetime.now(),
        piloto_id=1,
        aeronave_id=1,
        mision_id=mision.id
    )
    session.add(vuelo)
    session.commit()
    session.refresh(vuelo)

    tele = Telemetria(
        vuelo_id=vuelo.id,
        latitud=10,
        longitud=20,
        altitud=100,
        velocidad=50,
        timestamp=datetime.now()
    )
    session.add(tele)
    session.commit()
    session.refresh(tele)

    service = TelemetriaService(session)

    data = Telemetria(
        vuelo_id=vuelo.id,
        latitud=10,
        longitud=20,
        altitud=200,
        velocidad=80,
        timestamp=datetime.now()
    )

    with pytest.raises(Exception):
        service.update_telemetria_service(tele.id, data)

