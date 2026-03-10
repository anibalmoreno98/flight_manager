from sqlmodel import Session
from fastapi import HTTPException

from app.models.aeronave import Aeronave
from app.repositories import aeronave as aeronave_repo


def create_aeronave_service(aeronave: Aeronave, session: Session, repo=aeronave_repo):
    repo_instance = repo.AeronaveRepository(session)
    return repo_instance.add(aeronave)


def get_aeronave_service(aeronave_id: int, session: Session, repo=aeronave_repo):
    repo_instance = repo.AeronaveRepository(session)
    aeronave = repo_instance.get(aeronave_id)
    if not aeronave:
        raise HTTPException(status_code=404, detail="Aeronave no encontrada")
    return aeronave


def list_aeronaves_service(session: Session, repo=aeronave_repo):
    repo_instance = repo.AeronaveRepository(session)
    return repo_instance.list_all()


def update_aeronave_service(aeronave_id: int, aeronave_data: Aeronave, session: Session, repo=aeronave_repo):
    repo_instance = repo.AeronaveRepository(session)
    aeronave = repo_instance.get(aeronave_id)
    if not aeronave:
        raise HTTPException(status_code=404, detail="Aeronave no encontrada")

    aeronave.fabricante = aeronave_data.fabricante
    aeronave.modelo = aeronave_data.modelo
    aeronave.numero_serie = aeronave_data.numero_serie
    aeronave.velocidad_maxima = aeronave_data.velocidad_maxima

    return repo_instance.update(aeronave)


def delete_aeronave_service(aeronave_id: int, session: Session, repo=aeronave_repo):
    repo_instance = repo.AeronaveRepository(session)
    aeronave = repo_instance.get(aeronave_id)
    if not aeronave:
        raise HTTPException(status_code=404, detail="Aeronave no encontrada")

    repo_instance.delete(aeronave)
    return {"ok": True}
