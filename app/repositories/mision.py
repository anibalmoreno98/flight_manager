from typing import List
from sqlmodel import Session, select

from app.models.mision import Mision


def add(session: Session, mision: Mision) -> Mision:
    session.add(mision)
    session.commit()
    session.refresh(mision)
    return mision


def get(session: Session, mision_id: int) -> Mision | None:
    return session.get(Mision, mision_id)


def list_all(session: Session) -> List[Mision]:
    return session.exec(select(Mision)).all()


def update(session: Session, mision: Mision) -> Mision:
    session.add(mision)
    session.commit()
    session.refresh(mision)
    return mision


def delete(session: Session, mision: Mision) -> None:
    session.delete(mision)
    session.commit()
