from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from .usuario import Usuario
from .piloto import Piloto
from .aeronave import Aeronave
from .estado_mision import EstadoMision

class Mision(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None
    fecha_inicio: datetime
    fecha_fin: datetime

    estado: EstadoMision = Field(default=EstadoMision.CREADA)

    piloto_id: Optional[int] = Field(default=None, foreign_key="piloto.id")
    aeronave_id: Optional[int] = Field(default=None, foreign_key="aeronave.id")
    creado_por: int = Field(foreign_key="usuario.id")
