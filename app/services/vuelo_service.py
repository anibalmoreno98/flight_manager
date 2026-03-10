from sqlmodel import Session
from fastapi import HTTPException
from app.models.vuelo import Vuelo
from app.models.usuario import Usuario
from app.repositories import vuelo as vuelo_repo

def create_vuelo_service(vuelo: Vuelo, session: Session, repo=vuelo_repo):
    # Validar que el piloto/usuario existe
    usuario = session.get(Usuario, vuelo.piloto)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario (piloto) no encontrado")

    repo_instance = repo.VueloRepository(session)
    return repo_instance.add(vuelo)

def get_vuelo_service(vuelo_id: int, session: Session, repo=vuelo_repo):
    repo_instance = repo.VueloRepository(session)
    vuelo = repo_instance.get(vuelo_id)
    if not vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return vuelo

def list_vuelos_service(session: Session, repo=vuelo_repo):
    repo_instance = repo.VueloRepository(session)
    return repo_instance.list_all()

def update_vuelo_service(vuelo_id: int, vuelo_data: Vuelo, session: Session, repo=vuelo_repo):
    repo_instance = repo.VueloRepository(session)
    vuelo = repo_instance.get(vuelo_id)
    if not vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")

    # Actualizar campos
    vuelo.destino = vuelo_data.destino
    vuelo.fecha_inicio = vuelo_data.fecha_inicio
    vuelo.fecha_fin = vuelo_data.fecha_fin
    vuelo.piloto = vuelo_data.piloto
    vuelo.aeronave = vuelo_data.aeronave
    vuelo.telemetria = vuelo_data.telemetria

    return repo_instance.update(vuelo)

def delete_vuelo_service(vuelo_id: int, session: Session, repo=vuelo_repo):
    repo_instance = repo.VueloRepository(session)
    vuelo = repo_instance.get(vuelo_id)
    if not vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")

    repo_instance.delete(vuelo)
    return {"ok": True}
