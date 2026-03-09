from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.models.usuario import Usuario
from app.database import get_session
from app.services.usuario_service import (
    create_usuario_service,
    get_usuario_service,
    list_usuarios_service,
    update_usuario_service,
    delete_usuario_service,
)

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=Usuario)
def create_usuario(usuario: Usuario, session: Session = Depends(get_session)):
    return create_usuario_service(usuario, session)

@router.get("/", response_model=List[Usuario])
def read_usuarios(session: Session = Depends(get_session)):
    return list_usuarios_service(session)

@router.get("/{usuario_id}", response_model=Usuario)
def read_usuario(usuario_id: int, session: Session = Depends(get_session)):
    return get_usuario_service(usuario_id, session)

@router.put("/{usuario_id}", response_model=Usuario)
def update_usuario(usuario_id: int, usuario: Usuario, session: Session = Depends(get_session)):
    return update_usuario_service(usuario_id, usuario, session)

@router.delete("/{usuario_id}")
def delete_usuario(usuario_id: int, session: Session = Depends(get_session)):
    return delete_usuario_service(usuario_id, session)
