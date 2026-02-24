from sqlmodel import Session
from fastapi import HTTPException
from app.models.vuelo import Vuelo
from app.models.usuario import Usuario
from app.repositories import vuelo as vuelo_repo

def create_vuelo_service(vuelo: Vuelo, session: Session):
    # Validar que el piloto/usuario existe
    usuario = session.get(Usuario, vuelo.piloto)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario (piloto) no encontrado")

    return vuelo_repo.add(session, vuelo)

def get_vuelo_service(vuelo_id: int, session: Session):
    vuelo = vuelo_repo.get(session, vuelo_id)
    if not vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return vuelo

def list_vuelos_service(session: Session):
    return vuelo_repo.list_all(session)

def update_vuelo_service(vuelo_id: int, vuelo_data: Vuelo, session: Session):
    vuelo = vuelo_repo.get(session, vuelo_id)
    if not vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")

    # Actualizar campos
    vuelo.destino = vuelo_data.destino
    vuelo.fecha_inicio = vuelo_data.fecha_inicio
    vuelo.fecha_fin = vuelo_data.fecha_fin
    vuelo.piloto = vuelo_data.piloto
    vuelo.aeronave = vuelo_data.aeronave
    vuelo.telemetria = vuelo_data.telemetria

    return vuelo_repo.update(session, vuelo)

def delete_vuelo_service(vuelo_id: int, session: Session):
    vuelo = vuelo_repo.get(session, vuelo_id)
    if not vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")

    vuelo_repo.delete(session, vuelo)
    return {"ok": True}
