from sqlmodel import Session
from fastapi import HTTPException

from app.models.telemetria import Telemetria
from app.repositories import telemetria as telemetria_repo


def create_telemetria_service(telemetria: Telemetria, session: Session):
    return telemetria_repo.add(session, telemetria)


def get_telemetria_service(telemetria_id: int, session: Session):
    tele = telemetria_repo.get(session, telemetria_id)
    if not tele:
        raise HTTPException(status_code=404, detail="Telemetria no encontrada")
    return tele


def list_telemetria_service(session: Session):
    return telemetria_repo.list_all(session)


def update_telemetria_service(telemetria_id: int, telemetria_data: Telemetria, session: Session):
    tele = telemetria_repo.get(session, telemetria_id)
    if not tele:
        raise HTTPException(status_code=404, detail="Telemetria no encontrada")

    tele.altura_maxima = telemetria_data.altura_maxima
    tele.velocidad_maxima = telemetria_data.velocidad_maxima

    return telemetria_repo.update(session, tele)


def delete_telemetria_service(telemetria_id: int, session: Session):
    tele = telemetria_repo.get(session, telemetria_id)
    if not tele:
        raise HTTPException(status_code=404, detail="Telemetria no encontrada")

    telemetria_repo.delete(session, tele)
    return {"ok": True}
