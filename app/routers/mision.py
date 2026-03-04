from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_sesion
from app.models.mision import Mision
from app.services.mision_service import (
    create_mision_service,
    get_mision_service,
    list_misiones_service,
    update_mision_service,
    delete_mision_service,
)

router = APIRouter(prefix="/misiones", tags=["misiones"])

@router.post("/", response_model=Mision, status_code=201)
def create_mision(mision: Mision, session: Session = Depends(get_sesion)):
    return create_mision_service(mision, session)

@router.get("/", response_model=List[Mision], status_code=200)
def read_misiones(session: Session = Depends(get_sesion)):
    return list_misiones_service(session)

@router.get("/{mision_id}", response_model=Mision, status_code=200)
def read_mision(mision_id: int, session: Session = Depends(get_sesion)):
    return get_mision_service(mision_id, session)

@router.put("/{mision_id}", response_model=Mision, status_code=200)
def update_mision(mision_id: int, mision: Mision, session: Session = Depends(get_sesion)):
    return update_mision_service(mision_id, mision, session)

@router.delete("/{mision_id}", status_code=204)
def delete_mision(mision_id: int, session: Session = Depends(get_sesion)):
    return delete_mision_service(mision_id, session)
