from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.models.usuario import Usuario
from app.database import get_sesion
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=Usuario)
def create_usuario(usuario: Usuario, session: Session = Depends(get_sesion)):
    return UsuarioService(session).create_usuario_service(usuario)

@router.get("/", response_model=List[Usuario])
def read_usuarios(session: Session = Depends(get_sesion)):
    return UsuarioService(session).list_usuarios_service()

@router.get("/{usuario_id}", response_model=Usuario)
def read_usuario(usuario_id: int, session: Session = Depends(get_sesion)):
    return UsuarioService(session).get_usuario_service(usuario_id)

@router.put("/{usuario_id}", response_model=Usuario)
def update_usuario(usuario_id: int, usuario: Usuario, session: Session = Depends(get_sesion)):
    return UsuarioService(session).update_usuario_service(usuario_id, usuario)

@router.delete("/{usuario_id}")
def delete_usuario(usuario_id: int, session: Session = Depends(get_sesion)):
    return UsuarioService(session).delete_usuario_service(usuario_id)