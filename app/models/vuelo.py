

from dataclasses import Field
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class Vuelo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    piloto: int = Field(foreign_key="usuario.id")
    aeronave: str = Field(foreign_key="aeronave.id")
    telemetria: str = Field(foreign_key="telemetria.id")
    fecha_inicio: datetime
    fecha_fin: datetime