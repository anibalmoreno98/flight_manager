
from app.models.aeronave import Aeronave
from app.services.aeronave_service import create_aeronave_service, get_aeronave_service, update_aeronave_service

from unittest.mock import Mock

def test_create_aeronave_service():
    repo = Mock() # mock de la CLASE repositoro
    repo_instance = repo.return_value # mock de la INSTANCIA del repositorio
    session = Mock()

    # la aeronave la creamos, pero la session y el repo lo mockeamos
    aeronave = Aeronave(id=1, fabricante="Boeing", modelo="747", numero_serie="12345", velocidad_maxima=900.0)

    repo_instance.add.return_value = aeronave

    resultado = create_aeronave_service(aeronave, session, repo=repo)

    repo.assert_called_once_with(session) # el servicio instancio el repo
    repo_instance.add.assert_called_once_with(aeronave) # el metodo add fue llamado 

    assert resultado.id == 1

def test_get_aeronave_service():
    # creamos los parametros necesarios
    repo = Mock()
    session = Mock()
    aeronave = Aeronave(id=1, fabricante="Boeing", modelo="747", numero_serie="12345", velocidad_maxima=900.0)

    # mockeamos el metodo get del repo para que devuelva la aeronave creada
    repo.get.return_value = aeronave

    # llamamos al servicio y le añadimos los parmaetros de prueba
    resultado = get_aeronave_service(aeronave.id, session, repo=repo)

    # verificamos
    assert resultado.id == aeronave.id

def test_update_aeronave_service():
    # creamos los parametros necesarios
    repo = Mock()
    session = Mock()
    aeronave_actualizada = Aeronave(id=1, fabricante="Boeing", modelo="747", numero_serie="12345", velocidad_maxima=900.0)

    # mockeamos el get del metodo original para que devuelva la aeronave_actualizada (y el update)
    repo.get.return_value = aeronave_actualizada
    repo.update.return_value = aeronave_actualizada

    # mockeamos el metodo update del repo para que devuelva la aeronave actualizada
    resultado = update_aeronave_service(aeronave_id=1, aeronave_data=aeronave_actualizada, session=session, repo=repo)
    repo.update.assert_called_once_with(session, aeronave_actualizada)
    assert resultado.id == 1