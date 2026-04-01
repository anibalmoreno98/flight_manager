
import pytest



def test_crear_usuario(client):
    payload = {
        "nombre": "Test User",
        "username": "test_user",
        "password": "1234"
    }

    response = client.post("/usuarios/", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["id"] > 0
    assert data["username"] == "test_user"

def test_no_permite_username_duplicado(client):
    payload = {
        "nombre": "User1",
        "username": "duplicado",
        "password": "1234"
    }

    client.post("/usuarios/", json=payload)
    response = client.post("/usuarios/", json=payload)

    assert response.status_code == 400

def test_get_usuario_por_id(client):
    # Crear usuario
    res = client.post("/usuarios/", json={
        "nombre": "User Get",
        "username": "user_get",
        "password": "1234"
    })
    user_id = res.json()["id"]

    # Obtenerlo
    response = client.get(f"/usuarios/{user_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == user_id
    assert data["username"] == "user_get"

def test_listar_usuarios(client):
    client.post("/usuarios/", json={"nombre": "A", "username": "u1", "password": "1"})
    client.post("/usuarios/", json={"nombre": "B", "username": "u2", "password": "2"})

    response = client.get("/usuarios/")

    assert response.status_code == 200
    data = response.json()

    assert len(data) >= 2

def test_actualizar_usuario(client):
    # Crear usuario
    res = client.post("/usuarios/", json={
        "nombre": "Old",
        "username": "old_user",
        "password": "1234"
    })
    user_id = res.json()["id"]

    # Actualizar
    response = client.put(f"/usuarios/{user_id}", json={
        "nombre": "New",
        "username": "new_user",
        "password": "1234"
    })

    assert response.status_code == 200
    data = response.json()

    assert data["nombre"] == "New"
    assert data["username"] == "new_user"

def test_eliminar_usuario(client):
    # Crear usuario
    res = client.post("/usuarios/", json={
        "nombre": "Delete",
        "username": "delete_user",
        "password": "1234"
    })
    user_id = res.json()["id"]

    # Eliminar
    response = client.delete(f"/usuarios/{user_id}")

    assert response.status_code == 200
    assert response.json() == {"ok": True}

    # Verificar que ya no existe
    response2 = client.get(f"/usuarios/{user_id}")
    assert response2.status_code == 404

def test_login_correcto(client):
    # Crear usuario
    client.post("/usuarios/", json={
        "nombre": "Login",
        "username": "login_user",
        "password": "abcd"
    })

    # Login
    response = client.post("/auth/login", json={
        "username": "login_user",
        "password": "abcd"
    })

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data

def test_login_incorrecto(client):
    # Crear usuario
    client.post("/usuarios/", json={
        "nombre": "Login2",
        "username": "login_user2",
        "password": "abcd"
    })

    # Login con password incorrecta
    response = client.post("/auth/login", json={
        "username": "login_user2",
        "password": "wrong"
    })

    assert response.status_code == 401

