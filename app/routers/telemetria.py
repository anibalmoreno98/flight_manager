from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.models.telemetria import Telemetria
from app.services.telemetria_service import TelemetriaService

router = APIRouter(prefix="/telemetrias", tags=["telemetrias"])

@router.post("/", response_model=Telemetria)
def create_telemetria(telemetria: Telemetria, session: Session = Depends(get_session)):
    return TelemetriaService(session).create_telemetria_service(telemetria)

@router.get("/", response_model=List[Telemetria])
def read_telemetrias(session: Session = Depends(get_session)):
    return TelemetriaService(session).list_telemetria_service()

@router.get("/{telemetria_id}", response_model=Telemetria)
def read_telemetria(telemetria_id: int, session: Session = Depends(get_session)):
    return TelemetriaService(session).get_telemetria_service(telemetria_id)

@router.put("/{telemetria_id}", response_model=Telemetria)
def update_telemetria(telemetria_id: int, telemetria: Telemetria, session: Session = Depends(get_session)):
    return TelemetriaService(session).update_telemetria_service(telemetria_id, telemetria)

@router.delete("/{telemetria_id}")
def delete_telemetria(telemetria_id: int, session: Session = Depends(get_session)):
    return TelemetriaService(session).delete_telemetria_service(telemetria_id)
