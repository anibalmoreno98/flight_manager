



def test_crear_vuelo_guarda_en_bd(session):
    # Crear piloto
    piloto = Piloto(nombre="Juan", apellido="Pérez", licencia="LIC001")
    session.add(piloto)

    # Crear aeronave
    aeronave = Aeronave(fabricante="Boeing", modelo="737", numero_serie="SN1", velocidad_maxima=800)
    session.add(aeronave)

    # Crear misión activa
    mision = Mision(
        nombre="Misión Test",
        descripcion="Test",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now() + timedelta(hours=1),
        creado_por=1,
        estado=EstadoMision.EN_CURSO
    )
    session.add(mision)
    session.commit()

    service = VueloService(session)

    vuelo_data = Vuelo(
        origen="A",
        destino="B",
        fecha=datetime.now(),
        piloto_id=piloto.id,
        aeronave_id=aeronave.id,
        mision_id=mision.id
    )

    vuelo_creado = service.create_vuelo_service(vuelo_data)

    assert vuelo_creado.id is not None
    assert vuelo_creado.origen == "A"

def test_no_permite_crear_vuelo_con_piloto_inexistente(session):
    aeronave = Aeronave(fabricante="X", modelo="Y", numero_serie="SN2", velocidad_maxima=700)
    session.add(aeronave)

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

    service = VueloService(session)

    vuelo = Vuelo(
        origen="A",
        destino="B",
        fecha=datetime.now(),
        piloto_id=9999,  # inexistente
        aeronave_id=aeronave.id,
        mision_id=mision.id
    )

    with pytest.raises(Exception):
        service.create_vuelo_service(vuelo)

def test_no_permite_crear_vuelo_con_aeronave_inexistente(session):
    piloto = Piloto(nombre="Test", apellido="Pilot", licencia="LIC002")
    session.add(piloto)

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

    service = VueloService(session)

    vuelo = Vuelo(
        origen="A",
        destino="B",
        fecha=datetime.now(),
        piloto_id=piloto.id,
        aeronave_id=9999,  # inexistente
        mision_id=mision.id
    )

    with pytest.raises(Exception):
        service.create_vuelo_service(vuelo)

def test_no_permite_crear_vuelo_en_mision_finalizada(session):
    piloto = Piloto(nombre="Test", apellido="Pilot", licencia="LIC003")
    aeronave = Aeronave(fabricante="A", modelo="B", numero_serie="SN3", velocidad_maxima=750)
    session.add(piloto)
    session.add(aeronave)

    mision = Mision(
        nombre="Misión Finalizada",
        descripcion="Test",
        fecha_inicio=datetime.now(),
        fecha_fin=datetime.now(),
        creado_por=1,
        estado=EstadoMision.FINALIZADA
    )
    session.add(mision)
    session.commit()

    service = VueloService(session)

    vuelo = Vuelo(
        origen="A",
        destino="B",
        fecha=datetime.now(),
        piloto_id=piloto.id,
        aeronave_id=aeronave.id,
        mision_id=mision.id
    )

    with pytest.raises(Exception):
        service.create_vuelo_service(vuelo)

def test_actualizar_vuelo(session):
    piloto = Piloto(nombre="A", apellido="B", licencia="LIC004")
    aeronave = Aeronave(fabricante="X", modelo="Y", numero_serie="SN4", velocidad_maxima=700)
    session.add(piloto)
    session.add(aeronave)

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
        piloto_id=piloto.id,
        aeronave_id=aeronave.id,
        mision_id=mision.id
    )
    session.add(vuelo)
    session.commit()
    session.refresh(vuelo)

    service = VueloService(session)

    data = Vuelo(
        origen="A",
        destino="C",
        fecha=datetime.now(),
        piloto_id=piloto.id,
        aeronave_id=aeronave.id,
        mision_id=mision.id
    )

    vuelo_actualizado = service.update_vuelo_service(vuelo.id, data)

    assert vuelo_actualizado.destino == "C"

def test_no_permite_eliminar_vuelo_con_telemetria(session):
    piloto = Piloto(nombre="A", apellido="B", licencia="LIC005")
    aeronave = Aeronave(fabricante="X", modelo="Y", numero_serie="SN5", velocidad_maxima=700)
    session.add(piloto)
    session.add(aeronave)

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
        piloto_id=piloto.id,
        aeronave_id=aeronave.id,
        mision_id=mision.id
    )
    session.add(vuelo)
    session.commit()
    session.refresh(vuelo)

    tele = Telemetria(
        vuelo_id=vuelo.id,
        latitud=10.0,
        longitud=20.0,
        altitud=100.0,
        velocidad=50.0,
        timestamp=datetime.now()
    )
    session.add(tele)
    session.commit()

    service = VueloService(session)

    with pytest.raises(Exception):
        service.delete_vuelo_service(vuelo.id)

