from typing import List
from sqlmodel import Session, select

from app.models.telemetria import Telemetria


def add(session: Session, tele: Telemetria) -> Telemetria:
    session.add(tele)
    session.commit()
    session.refresh(tele)
    return tele


def get(session: Session, telemetria_id: int) -> Telemetria | None:
    return session.get(Telemetria, telemetria_id)


def list_all(session: Session) -> List[Telemetria]:
    return session.exec(select(Telemetria)).all()


def update(session: Session, tele: Telemetria) -> Telemetria:
    session.add(tele)
    session.commit()
    session.refresh(tele)
    return tele


def delete(session: Session, tele: Telemetria) -> None:
    session.delete(tele)
    session.commit()
