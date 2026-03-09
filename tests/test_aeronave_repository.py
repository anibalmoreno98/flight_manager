
# vamos a probar el metodo de add aeronave

# importamos el modelo aeronave y el repositorio de aeronave
from app.repositories import aeronave as aeronave_repo
from app.models.aeronave import Aeronave

def test_add_aeronave(session):
    nueva_aeronave = Aeronave(id=1, fabricante="Boeing", modelo="747", numero_serie="12345", velocidad_maxima=900.0)

    resultado = aeronave_repo.add(session, nueva_aeronave)

    assert resultado.id is not None


def test_delete_aeronave(session):
    nueva_aeronave = Aeronave(id=2, fabricante="Airbus", modelo="A320", numero_serie="67890", velocidad_maxima=800.0)

    # añadimos la aeronave para poder borrarla después
    aeronave_repo.add(session, nueva_aeronave)
    # la borramos
    aeronave_repo.delete(session, nueva_aeronave)
    # intentamos obtener la aeronave borrada
    resultado = aeronave_repo.get(session, nueva_aeronave.id)
    # el resultado debería ser None porque la aeronave fue borrada
    assert resultado is None