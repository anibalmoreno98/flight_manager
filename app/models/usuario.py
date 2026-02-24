

from typing import Optional

from pydantic import Field
from sqlmodel import SQLModel


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    username: str