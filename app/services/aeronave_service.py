from sqlmodel import Session
from fastapi import HTTPException

from app.models.aeronave import Aeronave
from app.repositories import aeronave as aeronave_repo


def create_aeronave_service(aeronave: Aeronave, session: Session):
    return aeronave_repo.add(session, aeronave)


def get_aeronave_service(aeronave_id: int, session: Session):
    aeronave = aeronave_repo.get(session, aeronave_id)
    if not aeronave:
        raise HTTPException(status_code=404, detail="Aeronave no encontrada")
    return aeronave


def list_aeronaves_service(session: Session):
    return aeronave_repo.list_all(session)


def update_aeronave_service(aeronave_id: int, aeronave_data: Aeronave, session: Session):
    aeronave = aeronave_repo.get(session, aeronave_id)
    if not aeronave:
        raise HTTPException(status_code=404, detail="Aeronave no encontrada")

    aeronave.fabricante = aeronave_data.fabricante
    aeronave.modelo = aeronave_data.modelo
    aeronave.numero_serie = aeronave_data.numero_serie
    aeronave.velocidad_maxima = aeronave_data.velocidad_maxima

    return aeronave_repo.update(session, aeronave)


def delete_aeronave_service(aeronave_id: int, session: Session):
    aeronave = aeronave_repo.get(session, aeronave_id)
    if not aeronave:
        raise HTTPException(status_code=404, detail="Aeronave no encontrada")

    aeronave_repo.delete(session, aeronave)
    return {"ok": True}
