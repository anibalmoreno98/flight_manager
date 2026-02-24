from sqlmodel import create_engine, Session

DATABASE_URL = "postgresql+psycopg://admin:admin@db:5432/flights"

engine = create_engine(DATABASE_URL, echo=True)

def get_sesion():
    with Session(engine) as session:
        yield session