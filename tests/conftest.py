import pytest
from sqlmodel import SQLModel, create_engine, Session

@pytest.fixture
def session():
    # Base de datos temporal en memoria
    engine = create_engine("sqlite:///:memory:", echo=False)
    # Importamos los modelos para que SQLModel conozca las tablas
    from app.models import usuario, aeronave, piloto, mision, vuelo, telemetria
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session