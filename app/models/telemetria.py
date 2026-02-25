

from typing import Optional

from sqlmodel import SQLModel, Field


class Telemetria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    altura_maxima: float
    velocidad_maxima: float