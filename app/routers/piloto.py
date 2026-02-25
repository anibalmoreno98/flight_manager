from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_sesion
from app.models.piloto import Piloto
from app.services.piloto_service import (
    create_piloto_service,
    get_piloto_service,
    list_pilotos_service,
    update_piloto_service,
    delete_piloto_service,
)

router = APIRouter(prefix="/pilotos", tags=["pilotos"])

@router.post("/", response_model=Piloto)
def create_piloto(piloto: Piloto, session: Session = Depends(get_sesion)):
    return create_piloto_service(piloto, session)

@router.get("/", response_model=List[Piloto])
def read_pilotos(session: Session = Depends(get_sesion)):
    return list_pilotos_service(session)

@router.get("/{piloto_id}", response_model=Piloto)
def read_piloto(piloto_id: int, session: Session = Depends(get_sesion)):
    return get_piloto_service(piloto_id, session)

@router.put("/{piloto_id}", response_model=Piloto)
def update_piloto(piloto_id: int, piloto: Piloto, session: Session = Depends(get_sesion)):
    return update_piloto_service(piloto_id, piloto, session)

@router.delete("/{piloto_id}")
def delete_piloto(piloto_id: int, session: Session = Depends(get_sesion)):
    return delete_piloto_service(piloto_id, session)
