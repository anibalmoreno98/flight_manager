from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.models.mision import Mision
from app.services.mision_service import MisionService
from app.security.dependencies import get_current_user
from app.security.roles import require_role
from app.models.usuario import Usuario

router = APIRouter(prefix="/misiones", tags=["misiones"])

@router.post("/", response_model=Mision)
def create_mision(
    mision: Mision,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(require_role("admin", "operador"))
):
    return MisionService(session).create_mision_service(mision)

@router.get("/", response_model=List[Mision])
def read_misiones(session: Session = Depends(get_session)):
    return MisionService(session).list_misiones_service()

@router.get("/{mision_id}", response_model=Mision)
def read_mision(mision_id: int, session: Session = Depends(get_session)):
    return MisionService(session).get_mision_service(mision_id)

@router.put("/{mision_id}", response_model=Mision)
def update_mision(
    mision_id: int,
    mision: Mision,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(require_role("admin", "operador"))
):
    return MisionService(session).update_mision_service(mision_id, mision)

@router.delete("/{mision_id}")
def delete_mision(
    mision_id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(require_role("admin"))
):
    return MisionService(session).delete_mision_service(mision_id)
