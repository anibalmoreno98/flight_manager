from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Telemetria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    vuelo_id: int = Field(foreign_key="vuelo.id")

    latitud: float
    longitud: float
    altitud: float
    velocidad: float

    altura_maxima: float
    velocidad_maxima: float

    timestamp: datetime
