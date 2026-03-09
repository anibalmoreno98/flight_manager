from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "postgresql+psycopg2://admin:admin@db:5432/flights"

# el engine se crea una sola vez y se reutiliza para todas las sesiones
engine = None

def get_engine():
    global engine
    if engine is None:
        engine = create_engine(DATABASE_URL, echo=True)
    return engine

def create_db_and_tables():
    from app.models import usuario, aeronave, piloto, mision, vuelo, telemetria
    SQLModel.metadata.create_all(get_engine())

def get_session():
    with Session(get_engine()) as session:
        yield session