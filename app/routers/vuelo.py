from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_sesion
from app.models.vuelo import Vuelo
from app.services.vuelo_service import (
    create_vuelo_service,
    get_vuelo_service,
    list_vuelos_service,
    update_vuelo_service,
    delete_vuelo_service,
)

router = APIRouter(prefix="/vuelos", tags=["vuelos"])

@router.post("/", response_model=Vuelo, status_code=201)
def create_vuelo(vuelo: Vuelo, session: Session = Depends(get_sesion)):
    return create_vuelo_service(vuelo, session)

@router.get("/", response_model=List[Vuelo], status_code=200)
def read_vuelos(session: Session = Depends(get_sesion)):
    return list_vuelos_service(session)

@router.get("/{vuelo_id}", response_model=Vuelo, status_code=200)
def read_vuelo(vuelo_id: int, session: Session = Depends(get_sesion)):
    return get_vuelo_service(vuelo_id, session)

@router.put("/{vuelo_id}", response_model=Vuelo, status_code=200)
def update_vuelo(vuelo_id: int, vuelo: Vuelo, session: Session = Depends(get_sesion)):
    return update_vuelo_service(vuelo_id, vuelo, session)

@router.delete("/{vuelo_id}", status_code=204)
def delete_vuelo(vuelo_id: int, session: Session = Depends(get_sesion)):
    return delete_vuelo_service(vuelo_id, session)
