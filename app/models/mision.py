
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Mision(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None
    fecha_inicio: datetime
    fecha_fin: datetime
    creado_por: int =Field(foreign_key="usuario.id")