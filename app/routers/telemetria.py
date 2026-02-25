from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_sesion
from app.models.telemetria import Telemetria
from app.services.telemetria_service import (
    create_telemetria_service,
    get_telemetria_service,
    list_telemetria_service,
    update_telemetria_service,
    delete_telemetria_service,
)

router = APIRouter(prefix="/telemetrias", tags=["telemetrias"])

@router.post("/", response_model=Telemetria)
def create_telemetria(telemetria: Telemetria, session: Session = Depends(get_sesion)):
    return create_telemetria_service(telemetria, session)

@router.get("/", response_model=List[Telemetria])
def read_telemetrias(session: Session = Depends(get_sesion)):
    return list_telemetria_service(session)

@router.get("/{telemetria_id}", response_model=Telemetria)
def read_telemetria(telemetria_id: int, session: Session = Depends(get_sesion)):
    return get_telemetria_service(telemetria_id, session)

@router.put("/{telemetria_id}", response_model=Telemetria)
def update_telemetria(telemetria_id: int, telemetria: Telemetria, session: Session = Depends(get_sesion)):
    return update_telemetria_service(telemetria_id, telemetria, session)

@router.delete("/{telemetria_id}")
def delete_telemetria(telemetria_id: int, session: Session = Depends(get_sesion)):
    return delete_telemetria_service(telemetria_id, session)
