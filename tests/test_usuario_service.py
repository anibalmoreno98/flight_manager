from unittest.mock import Mock

from app.services.usuario_service import create_usuario_service, get_usuario_service, list_usuarios_service, update_usuario_service # traemos el service.usuario_service
from app.models.usuario import Usuario # traemos el modelo de usuario para crear instancias de usuario en las pruebas

# esta funcion debe comprobar que el servicio de crear usuario funciona correctamente
def test_create_usuario_service():
    repo = Mock() # creamos un mock del repositorio para simular la base de datos
    session = Mock() # creamos un mock de la sesión para simular la conexión a la base de datos
    usuario = Usuario(nombre="Ana") # creamos una instancia de usuario con el nombre "Ana"

    repo.add.return_value = Usuario(id=1, nombre="Ana") # significa: cuando alguien llame a repo.add, devuelve un usuario con id 1 y nombre "Ana"

    resultado = create_usuario_service(usuario, session, repo=repo)
    repo.add.assert_called_once_with(session, usuario) # verificamos que repo.add fue llamado una vez con la sesión y el usuario
    assert resultado.id == 1 # verificamos que el resultado tiene el id 1

def test_list_usuarios_service():
    repo = Mock() # creamos un mock del repositorio
    session = Mock() # creamos un mock de la sesión

    repo.list_all.return_value = [Usuario(id=1, nombre="Ana"), Usuario(id=2, nombre="Luis")] # cuando alguien llame a repo.list_all, devuelve una lista de usuarios

    resultado = list_usuarios_service(session, repo=repo) # llamamos al servicio de listar usuarios con la sesión y el repositorio mockeado
    repo.list_all.assert_called_once_with(session) # verificamos que repo.list_all fue llamado una vez con la sesión

    assert len(resultado) == 2 # verificamos que el resultado tiene 2 usuarios

def test_get_usuario_service():
    repo = Mock()
    session = Mock()
    usuario_id = 1

    repo.get.return_value = Usuario(id=usuario_id, nombre="Ana") # cuando alguien llame a repo.get con el id 1, devuelve un usuario con ese id y nombre "Ana"

    resultado = get_usuario_service(usuario_id, session, repo=repo) # llamamos al servicio de obtener usuario con el id, la sesión y el repositorio mockeado
    repo.get.assert_called_once_with(session, usuario_id) # verificamos que repo.get fue llamado una vez con la sesión y el id del usuario
    assert resultado.id == usuario_id # verificamos que el resultado tiene el id correcto


def test_update_usuario_service():
    repo = Mock()
    session = Mock()
    usuario_id = 1
    usuario_data = Usuario(nombre="Ana", username="ana123") # creamos una instancia de usuario con el nombre "Ana" y username "ana123"

    repo.get.return_value = Usuario(id=usuario_id, nombre="Ana", username="ana123") # cuando alguien llame a repo.get con el id 1, devuelve un usuario con ese id, nombre "Ana" y username "ana123"
    repo.update.return_value = Usuario(id=usuario_id, nombre="AnaActualizado", username="ana123") # cuando alguien llame a repo.update con el usuario actualizado, devuelve un usuario con el nombre actualizado

    resultado = update_usuario_service(usuario_id, usuario_data, session, repo=repo) # llamamos al servicio de actualizar usuario con el id, los datos del usuario, la sesión y el repositorio mockeado

    repo.get.assert_called_once_with(session, usuario_id) # verificamos que repo.get fue llamado una vez con la sesión y el id del usuario
    repo.update.assert_called_once() # verificamos que repo.update fue llamado una vez
    assert resultado.nombre == "AnaActualizado" # verificamos que el resultado tiene el nombre actualizado


