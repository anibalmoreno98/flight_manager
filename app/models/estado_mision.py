from enum import Enum

class EstadoMision(str, Enum):
    CREADA = "CREADA"
    PLANIFICADA = "PLANIFICADA"
    EN_CURSO = "EN_CURSO"
    FINALIZADA = "FINALIZADA"
    CANCELADA = "CANCELADA"
