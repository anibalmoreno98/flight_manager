def mock_usuario():
    return {
        "nombre": "Usuario Test",
        "username": "usuario_test",
        "email": "usuario@test.com"
    }


def mock_aeronave():
    return {
        "fabricante": "Boeing",
        "modelo": "747",
        "numero_serie": "ABC123",
        "velocidad_maxima": 900.0
    }


def mock_piloto():
    return {
        "nombre": "Juan",
        "apellido": "Pérez",
        "licencia": "LIC123"
    }


def mock_telemetria():
    return {
        "altura_maxima": 10000.0,
        "velocidad_maxima": 850.0
    }


def mock_mision():
    return {
        "nombre": "Misión Test",
        "descripcion": "Descripción de prueba",
        "fecha_inicio": "2024-01-01T10:00:00",
        "fecha_fin": "2024-01-01T12:00:00",
        "creado_por": 1
    }


def mock_vuelo():
    return {
        "nombre": "Vuelo Test",
        "piloto": 1,
        "aeronave": 1,
        "telemetria": None,
        "fecha_inicio": "2024-01-01T09:00:00",
        "fecha_fin": "2024-01-01T11:00:00"
    }
