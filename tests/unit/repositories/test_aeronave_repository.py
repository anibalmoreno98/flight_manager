


from app.models.aeronave import Aeronave
from app.repositories.aeronave import AeronaveRepository


def test_aeronave_repository_add(session):
    repo = AeronaveRepository(session)

    aeronave = Aeronave(fabricante="Boeing", modelo="737", numero_serie="SN1", velocidad_maxima=800)
    creada = repo.add(aeronave)

    assert creada.id is not None


def test_aeronave_repository_get(session):
    aeronave = Aeronave(fabricante="Airbus", modelo="A320", numero_serie="SN2", velocidad_maxima=830)
    session.add(aeronave)
    session.commit()
    session.refresh(aeronave)

    repo = AeronaveRepository(session)
    obtenida = repo.get(aeronave.id)

    assert obtenida.id == aeronave.id


def test_aeronave_repository_list(session):
    session.add(Aeronave(fabricante="A", modelo="M1", numero_serie="S1", velocidad_maxima=700))
    session.add(Aeronave(fabricante="B", modelo="M2", numero_serie="S2", velocidad_maxima=750))
    session.commit()

    repo = AeronaveRepository(session)
    lista = repo.list_all()

    assert len(lista) == 2


def test_aeronave_repository_update(session):
    aeronave = Aeronave(fabricante="Old", modelo="X", numero_serie="SN3", velocidad_maxima=700)
    session.add(aeronave)
    session.commit()
    session.refresh(aeronave)

    repo = AeronaveRepository(session)
    aeronave.fabricante = "New"
    actualizada = repo.update(aeronave)

    assert actualizada.fabricante == "New"


def test_aeronave_repository_delete(session):
    aeronave = Aeronave(fabricante="Delete", modelo="X", numero_serie="SN4", velocidad_maxima=700)
    session.add(aeronave)
    session.commit()
    session.refresh(aeronave)

    repo = AeronaveRepository(session)
    repo.delete(aeronave)

    assert session.get(Aeronave, aeronave.id) is None
