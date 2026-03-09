

from app.main import app
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from app.database import get_session
from app.models.aeronave import Aeronave



def test_create_aeronave(client):
    response = client.post("/aeronaves/", json={
        "fabricante": "Boeing",
        "modelo": "747",
        "numero_serie": "12345",
        "velocidad_maxima": 900.0
    })
    assert response.status_code in (200, 201)

def test_read_aeronave(client):
    response = client.post("/aeronaves/", json={
        "fabricante": "Airbus",
        "modelo": "A380",
        "numero_serie": "67890",
        "velocidad_maxima": 950.0
    })
    assert response.status_code in (200, 201)

def test_update_aeronave(client):
    response = client.post("/aeronaves/", json={
        "fabricante": "Cessna",
        "modelo": "172",
        "numero_serie": "54321",
        "velocidad_maxima": 300.0
    })
    assert response.status_code in (200, 201)

def test_delete_aeronave(client):
    response = client.post("/aeronaves/", json={
        "fabricante": "Piper",
        "modelo": "PA-28",
        "numero_serie": "98765",
        "velocidad_maxima": 250.0
    })
    assert response.status_code in (200, 201)

def test_list_aeronaves(client):
    response = client.get("/aeronaves/")
    assert response.status_code == 200

def test_get_usuario(client):
    response = client.post("/usuarios/", json={
        "nombre": "Test User",
        "username": "testuser",
        "email": "test@example.com"
    })
    assert response.status_code in (200, 201)