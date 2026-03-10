from sqlmodel import Session
from fastapi import HTTPException

from app.models.telemetria import Telemetria
from app.repositories import telemetria as telemetria_repo


def create_telemetria_service(telemetria: Telemetria, session: Session, repo=telemetria_repo):
    repo_instance = repo.TelemetriaRepository(session)
    return repo_instance.add(telemetria)


def get_telemetria_service(telemetria_id: int, session: Session, repo=telemetria_repo):
    repo_instance = repo.TelemetriaRepository(session)
    telemetria = repo_instance.get(telemetria_id)
    if not telemetria:
        raise HTTPException(status_code=404, detail="Telemetria no encontrada")
    return telemetria


def list_telemetria_service(session: Session, repo=telemetria_repo):
    repo_instance = repo.TelemetriaRepository(session)
    return repo_instance.list_all()


def update_telemetria_service(telemetria_id: int, telemetria_data: Telemetria, session: Session, repo=telemetria_repo):
    repo_instance = repo.TelemetriaRepository(session)
    telemetria = repo_instance.get(telemetria_id)
    if not telemetria:
        raise HTTPException(status_code=404, detail="Telemetria no encontrada")

    telemetria.altura_maxima = telemetria_data.altura_maxima
    telemetria.velocidad_maxima = telemetria_data.velocidad_maxima

    return repo_instance.update(telemetria)


def delete_telemetria_service(telemetria_id: int, session: Session, repo=telemetria_repo):
    repo_instance = repo.TelemetriaRepository(session)
    telemetria = repo_instance.get(telemetria_id)
    if not telemetria:
        raise HTTPException(status_code=404, detail="Telemetria no encontrada")

    repo_instance.delete(telemetria)
    return {"ok": True}