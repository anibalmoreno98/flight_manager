from sqlmodel import create_engine, SQLModel, Session

from app.models.usuario import Usuario
from app.models.aeronave import Aeronave
from app.models.piloto import Piloto
from app.models.telemetria import Telemetria
from app.models.mision import Mision
from app.models.vuelo import Vuelo

TEST_DB_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False}
)

def create_test_db():
    # Cerrar conexiones previas
    engine.dispose()

    # Recrear tablas
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def get_test_session():
    with Session(engine) as session:
        yield session
