from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.models.vuelo import Vuelo
from app.services.vuelo_service import VueloService

router = APIRouter(prefix="/vuelos", tags=["vuelos"])

@router.post("/", response_model=Vuelo)
def create_vuelo(vuelo: Vuelo, session: Session = Depends(get_session)):
    return VueloService(session).create_vuelo_service(vuelo)

@router.get("/", response_model=List[Vuelo])
def read_vuelos(session: Session = Depends(get_session)):
    return VueloService(session).list_vuelos_service()

@router.get("/{vuelo_id}", response_model=Vuelo)
def read_vuelo(vuelo_id: int, session: Session = Depends(get_session)):
    return VueloService(session).get_vuelo_service(vuelo_id)

@router.put("/{vuelo_id}", response_model=Vuelo)
def update_vuelo(vuelo_id: int, vuelo: Vuelo, session: Session = Depends(get_session)):
    return VueloService(session).update_vuelo_service(vuelo_id, vuelo)

@router.delete("/{vuelo_id}")
def delete_vuelo(vuelo_id: int, session: Session = Depends(get_session)):
    return VueloService(session).delete_vuelo_service(vuelo_id)