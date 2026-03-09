from app.models.vuelo import Vuelo
from app.repositories import vuelo as vuelo_repo

from datetime import datetime


def test_add_vuelo(session):
    # crear un nuevo vuelo con las FK necesarias
    nuevo_vuelo = Vuelo(id=1,
    nombre="Vuelo 1",
    piloto=1,
    aeronave=1,
    telemetria=1,
    fecha_inicio=datetime(2024, 12, 1),
    fecha_fin=datetime(2024, 12, 1))
    # llamamos al metodo original y le metemos los datos del nuevo vuelo
    resultado = vuelo_repo.add(session, nuevo_vuelo)
    # verificamos que dicho vuelo se haya creado correctamente
    assert resultado.id is not None

