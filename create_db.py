# create_db.py

from sqlmodel import SQLModel
from app.database import engine

from app.models.aeronave import Aeronave
from app.models.piloto import Piloto
from app.models.usuario import Usuario
from app.models.vuelo import Vuelo
from app.models.telemetria import Telemetria
from app.models.mision import Mision

# importa todos tus modelos para que SQLModel los registre

print("Creando tablas...")
SQLModel.metadata.create_all(engine)
print("Tablas creadas.")
