from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "postgresql+psycopg2://admin:admin@db:5432/flights"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    from app.models import usuario, aeronave, piloto, mision, vuelo, telemetria
    SQLModel.metadata.create_all(engine)

def get_sesion():
    with Session(engine) as session:
        yield session