from unittest.mock import Mock

import pytest

from app.services.usuario_service import create_usuario_service # traemos el service.usuario_service
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

    
    

    resultado = list_usuarios_service(session, repo=repo) # llamamos al servicio de listar usuarios con la sesión y el repositorio mockeado
