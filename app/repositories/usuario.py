from typing import List
from sqlmodel import Session, select
from app.models.usuario import Usuario

class UsuarioRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(self, usuario: Usuario) -> Usuario:
        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def get(self, usuario_id: int) -> Usuario | None:
        return self.session.get(Usuario, usuario_id)

    def list_all(self) -> List[Usuario]:
        return self.session.exec(select(Usuario)).all()

    def update(self, usuario: Usuario) -> Usuario:
        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def delete(self, usuario: Usuario) -> None:
        self.session.delete(usuario)
        self.session.commit()

    def get_by_username(self, username: str) -> Usuario | None:
        statement = select(Usuario).where(Usuario.username == username)
        return self.session.exec(statement).first()