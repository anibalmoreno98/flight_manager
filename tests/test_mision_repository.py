
# vamos a crear un test para probar el metodo add mision
import datetime
from app.repositories import mision
from app.models.mision import Mision

def test_add_mision(session):
    nueva_mision = Mision(nombre="Mision 1",
    descripcion="Descripcion de la mision 1",
    fecha_inicio=datetime.datetime(2024, 1, 1),
    fecha_fin=datetime.datetime(2024, 1, 31),
    creado_por=1)

    resultado = mision.add(session, nueva_mision)

    assert resultado.id is not None

def test_get_mision(session):
    nueva_mision = Mision(id=2,
    nombre="Mision 2",
    descripcion="Descripcion de la mision 2",
    fecha_inicio=datetime.datetime(2024, 2, 1),
    fecha_fin=datetime.datetime(2024, 2, 28),
    creado_por=1)

    mision.add(session, nueva_mision)

    resultado = mision.get(session, nueva_mision.id)

    assert resultado is not None