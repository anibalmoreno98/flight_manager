from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.models.aeronave import Aeronave
from app.services.aeronave_service import AeronaveService

router = APIRouter(prefix="/aeronaves", tags=["aeronaves"])

@router.post("/", response_model=Aeronave)
def create_aeronave(aeronave: Aeronave, session: Session = Depends(get_session)):
    return AeronaveService(session).create_aeronave_service(aeronave)

@router.get("/", response_model=List[Aeronave])
def read_aeronaves(session: Session = Depends(get_session)):
    return AeronaveService(session).list_aeronaves_service()

@router.get("/{aeronave_id}", response_model=Aeronave)
def read_aeronave(aeronave_id: int, session: Session = Depends(get_session)):
    return AeronaveService(session).get_aeronave_service(aeronave_id)

@router.put("/{aeronave_id}", response_model=Aeronave)
def update_aeronave(aeronave_id: int, aeronave: Aeronave, session: Session = Depends(get_session)):
    return AeronaveService(session).update_aeronave_service(aeronave_id, aeronave)

@router.delete("/{aeronave_id}")
def delete_aeronave(aeronave_id: int, session: Session = Depends(get_session)):
    return AeronaveService(session).delete_aeronave_service(aeronave_id)
