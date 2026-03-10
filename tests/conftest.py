import os
os.environ["TESTING"] = "1"

import pytest

# 1. Importar engine de test y set_engine ANTES de cargar la app
from tests.assets.db_test import engine as test_engine, create_test_db, get_test_session
from app.database import set_engine, get_session

# 2. Forzar que FastAPI use el engine de test ANTES de cargar la app
set_engine(test_engine)

# 3. Ahora sí, importar la app
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="function")
def client():
    # Crear tablas en el engine de test
    create_test_db()

    # Override de sesión
    app.dependency_overrides[get_session] = get_test_session

    # Crear cliente
    with TestClient(app) as c:
        yield c
