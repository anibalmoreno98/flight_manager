from fastapi import Depends, HTTPException, status
from app.security.dependencies import get_current_user
from app.models.usuario import Usuario

def require_role(*roles_permitidos: str):
    def wrapper(current_user: Usuario = Depends(get_current_user)):
        if current_user.rol not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción."
            )
        return current_user
    return wrapper
