from typing import List
from sqlmodel import Session, select

from app.models.aeronave import Aeronave


def add(session: Session, aeronave: Aeronave) -> Aeronave:
    session.add(aeronave)
    session.commit()
    session.refresh(aeronave)
    return aeronave


def get(session: Session, aeronave_id: int) -> Aeronave | None:
    return session.get(Aeronave, aeronave_id)


def list_all(session: Session) -> List[Aeronave]:
    return session.exec(select(Aeronave)).all()


def update(session: Session, aeronave: Aeronave) -> Aeronave:
    session.add(aeronave)
    session.commit()
    session.refresh(aeronave)
    return aeronave


def delete(session: Session, aeronave: Aeronave) -> None:
    session.delete(aeronave)
    session.commit()
