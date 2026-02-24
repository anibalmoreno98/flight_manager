

from typing import Optional

from pydantic import Field
from sqlmodel import SQLModel


class Piloto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    licencia: str