from fastapi import APIRouter, HTTPException
from sqlmodel import Session

from app.security.jwt import create_access_token
from app.security.password import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(self, username: str, password: str):
    usuario = self.repo.get_by_username(username)

    if not usuario or not verify_password(password, usuario.password):
        raise HTTPException(401, "Credenciales inválidas.")

    access_token = create_access_token({
        "sub": usuario.username,
        "rol": usuario.rol
    })

    return {"access_token": access_token, "token_type": "bearer"}
