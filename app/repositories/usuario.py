from typing import List
from sqlmodel import Session, select

from app.models.usuario import Usuario


def add(session: Session, usuario: Usuario) -> Usuario:
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


def get(session: Session, usuario_id: int) -> Usuario | None:
    return session.get(Usuario, usuario_id)


def list_all(session: Session) -> List[Usuario]:
    return session.exec(select(Usuario)).all()


def update(session: Session, usuario: Usuario) -> Usuario:
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


def delete(session: Session, usuario: Usuario) -> None:
    session.delete(usuario)
    session.commit()
