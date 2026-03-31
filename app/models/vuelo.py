from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Vuelo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str

    piloto_id: int = Field(foreign_key="piloto.id")
    aeronave_id: int = Field(foreign_key="aeronave.id")
    mision_id: int = Field(foreign_key="mision.id")

    fecha_inicio: datetime
    fecha_fin: datetime
