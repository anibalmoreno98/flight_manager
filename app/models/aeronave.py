

from typing import Optional

from pydantic import Field
from sqlmodel import SQLModel


class Aeronave(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fabricante: str
    modelo: str
    numero_serie: str
    velocidad_maxima: float
    