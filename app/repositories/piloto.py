from typing import List
from sqlmodel import Session, select

from app.models.piloto import Piloto


def add(session: Session, piloto: Piloto) -> Piloto:
    session.add(piloto)
    session.commit()
    session.refresh(piloto)
    return piloto


def get(session: Session, piloto_id: int) -> Piloto | None:
    return session.get(Piloto, piloto_id)


def list_all(session: Session) -> List[Piloto]:
    return session.exec(select(Piloto)).all()


def update(session: Session, piloto: Piloto) -> Piloto:
    session.add(piloto)
    session.commit()
    session.refresh(piloto)
    return piloto


def delete(session: Session, piloto: Piloto) -> None:
    session.delete(piloto)
    session.commit()
