

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Vuelo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    piloto: int = Field(foreign_key="usuario.id")
    aeronave: int = Field(foreign_key="aeronave.id")
    telemetria: int = Field(foreign_key="telemetria.id")
    fecha_inicio: datetime
    fecha_fin: datetime