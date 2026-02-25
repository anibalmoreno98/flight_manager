from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_sesion
from app.models.aeronave import Aeronave
from app.services.aeronave_service import (
    create_aeronave_service,
    get_aeronave_service,
    list_aeronaves_service,
    update_aeronave_service,
    delete_aeronave_service,
)

router = APIRouter(prefix="/aeronaves", tags=["aeronaves"])

@router.post("/", response_model=Aeronave)
def create_aeronave(aeronave: Aeronave, session: Session = Depends(get_sesion)):
    return create_aeronave_service(aeronave, session)

@router.get("/", response_model=List[Aeronave])
def read_aeronaves(session: Session = Depends(get_sesion)):
    return list_aeronaves_service(session)

@router.get("/{aeronave_id}", response_model=Aeronave)
def read_aeronave(aeronave_id: int, session: Session = Depends(get_sesion)):
    return get_aeronave_service(aeronave_id, session)

@router.put("/{aeronave_id}", response_model=Aeronave)
def update_aeronave(aeronave_id: int, aeronave: Aeronave, session: Session = Depends(get_sesion)):
    return update_aeronave_service(aeronave_id, aeronave, session)

@router.delete("/{aeronave_id}")
def delete_aeronave(aeronave_id: int, session: Session = Depends(get_sesion)):
    return delete_aeronave_service(aeronave_id, session)
