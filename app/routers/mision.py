from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_sesion
from app.models.mision import Mision
from app.services.mision_service import MisionService

router = APIRouter(prefix="/misiones", tags=["misiones"])

@router.post("/", response_model=Mision)
def create_mision(mision: Mision, session: Session = Depends(get_sesion)):
    return MisionService(session).create_mision_service(mision)

@router.get("/", response_model=List[Mision])
def read_misiones(session: Session = Depends(get_sesion)):
    return MisionService(session).list_misiones_service(session)

@router.get("/{mision_id}", response_model=Mision)
def read_mision(mision_id: int, session: Session = Depends(get_sesion)):
    return MisionService(session).get_mision_service(mision_id, session)

@router.put("/{mision_id}", response_model=Mision)
def update_mision(mision_id: int, mision: Mision, session: Session = Depends(get_sesion)):
    return MisionService(session).update_mision_service(mision_id, mision, session)

@router.delete("/{mision_id}")
def delete_mision(mision_id: int, session: Session = Depends(get_sesion)):
    return MisionService(session).delete_mision_service(mision_id, session)
