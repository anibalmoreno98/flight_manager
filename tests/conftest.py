import os
os.environ["TESTING"] = "1"

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from app.database import get_session

@pytest.fixture(scope="function")
def client():
    # 1. Crear engine SQLite en memoria
    engine = create_engine("sqlite:///:memory:")

    # 2. Sobrescribir get_session
    def override_get_session():
        # Crear tablas justo antes de abrir la asesión
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    # 4. Crear cliente
    with TestClient(app) as c:
        yield c
