import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_sesion

# Crear una base de datos en memoria para pruebas
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_sesion] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_aeronave(client: TestClient):
    response = client.post(
        "/aeronaves/",
        json={
            "fabricante": "Boeing",
            "modelo": "737",
            "numero_serie": "12345",
            "velocidad_maxima": 800.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["fabricante"] == "Boeing"
    assert "id" in data

def test_read_aeronaves(client: TestClient):
    # Primero crear una
    client.post(
        "/aeronaves/",
        json={
            "fabricante": "Airbus",
            "modelo": "A320",
            "numero_serie": "67890",
            "velocidad_maxima": 850.0
        }
    )
    response = client.get("/aeronaves/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_read_aeronave(client: TestClient):
    # Crear y obtener
    create_response = client.post(
        "/aeronaves/",
        json={
            "fabricante": "Boeing",
            "modelo": "747",
            "numero_serie": "11111",
            "velocidad_maxima": 900.0
        }
    )
    aeronave_id = create_response.json()["id"]
    response = client.get(f"/aeronaves/{aeronave_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["modelo"] == "747"

def test_update_aeronave(client: TestClient):
    # Crear
    create_response = client.post(
        "/aeronaves/",
        json={
            "fabricante": "Boeing",
            "modelo": "777",
            "numero_serie": "22222",
            "velocidad_maxima": 950.0
        }
    )
    aeronave_id = create_response.json()["id"]
    # Actualizar
    response = client.put(
        f"/aeronaves/{aeronave_id}",
        json={
            "fabricante": "Boeing",
            "modelo": "777 Updated",
            "numero_serie": "22222",
            "velocidad_maxima": 960.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["modelo"] == "777 Updated"

def test_delete_aeronave(client: TestClient):
    # Crear
    create_response = client.post(
        "/aeronaves/",
        json={
            "fabricante": "Airbus",
            "modelo": "A380",
            "numero_serie": "33333",
            "velocidad_maxima": 1000.0
        }
    )
    aeronave_id = create_response.json()["id"]
    # Eliminar
    response = client.delete(f"/aeronaves/{aeronave_id}")
    assert response.status_code == 200
    # Verificar que ya no existe
    get_response = client.get(f"/aeronaves/{aeronave_id}")
    assert get_response.status_code == 404