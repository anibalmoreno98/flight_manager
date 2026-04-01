import os
import tempfile
import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_session


@pytest.fixture
def test_engine():
    # Crear archivo SQLite temporal por test
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)

    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False}
    )

    # Crear tablas para este test
    SQLModel.metadata.create_all(engine)

    yield engine

    # Cerrar conexiones y borrar archivo
    engine.dispose()
    os.remove(db_path)


@pytest.fixture
def session(test_engine):
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
