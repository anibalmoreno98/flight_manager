from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    from app.models import usuario, aeronave, piloto, mision, vuelo, telemetria
    SQLModel.metadata.create_all(engine)

def get_sesion():
    with Session(engine) as session:
        yield session
