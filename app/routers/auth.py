from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(data: dict, session: Session = Depends(get_session)):
    username = data.get("username")
    password = data.get("password")

    return UsuarioService(session).login(username, password)
