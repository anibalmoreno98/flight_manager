from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.models.piloto import Piloto
from app.services.piloto_service import PilotoService

router = APIRouter(prefix="/pilotos", tags=["pilotos"])

@router.post("/", response_model=Piloto)
def create_piloto(piloto: Piloto, session: Session = Depends(get_session)):
    return PilotoService(session).create_piloto_service(piloto)

@router.get("/", response_model=List[Piloto])
def read_pilotos(session: Session = Depends(get_session)):
    return PilotoService(session).list_pilotos_service()

@router.get("/{piloto_id}", response_model=Piloto)
def read_piloto(piloto_id: int, session: Session = Depends(get_session)):
    return PilotoService(session).get_piloto_service(piloto_id)

@router.put("/{piloto_id}", response_model=Piloto)
def update_piloto(piloto_id: int, piloto: Piloto, session: Session = Depends(get_session)):
    return PilotoService(session).update_piloto_service(piloto_id, piloto)

@router.delete("/{piloto_id}")
def delete_piloto(piloto_id: int, session: Session = Depends(get_session)):
    return PilotoService(session).delete_piloto_service(piloto_id)
