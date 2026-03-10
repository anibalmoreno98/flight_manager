
from tests.assets.mock_data import mock_aeronave, mock_usuario


def test_create_aeronave(client):
    response = client.post("/aeronaves/", json=mock_aeronave())
    assert response.status_code in (200, 201)


def test_read_aeronave(client):
    # Crear aeronave primero
    aeronave = mock_aeronave()
    client.post("/aeronaves/", json=aeronave)

    response = client.get("/aeronaves/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_aeronave(client):
    # Crear aeronave
    create_resp = client.post("/aeronaves/", json=mock_aeronave())
    aeronave_id = create_resp.json()["id"]

    # Actualizar aeronave
    updated_data = {
        "fabricante": "Cessna",
        "modelo": "172",
        "numero_serie": "54321",
        "velocidad_maxima": 300.0
    }

    response = client.put(f"/aeronaves/{aeronave_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["modelo"] == "172"


def test_delete_aeronave(client):
    # Crear aeronave
    create_resp = client.post("/aeronaves/", json=mock_aeronave())
    aeronave_id = create_resp.json()["id"]

    # Borrar aeronave
    response = client.delete(f"/aeronaves/{aeronave_id}")
    assert response.status_code == 200


def test_list_aeronaves(client):
    client.post("/aeronaves/", json=mock_aeronave())
    response = client.get("/aeronaves/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_usuario(client):
    response = client.post("/usuarios/", json=mock_usuario())
    assert response.status_code in (200, 201)
