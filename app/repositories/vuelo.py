from typing import List, Optional
from sqlmodel import Session, select

from app.models.vuelo import Vuelo


def add(session: Session, vuelo: Vuelo) -> Vuelo:
    session.add(vuelo)
    session.commit()
    session.refresh(vuelo)
    return vuelo


def get(session: Session, vuelo_id: int) -> Optional[Vuelo]:
    return session.get(Vuelo, vuelo_id)


def list_all(session: Session) -> List[Vuelo]:
    return session.exec(select(Vuelo)).all()


def update(session: Session, vuelo: Vuelo) -> Vuelo:
    session.add(vuelo)
    session.commit()
    session.refresh(vuelo)
    return vuelo


def delete(session: Session, vuelo: Vuelo) -> None:
    session.delete(vuelo)
    session.commit()

# additional helpers

def list_by_piloto(session: Session, piloto_id: int) -> List[Vuelo]:
    statement = select(Vuelo).where(Vuelo.piloto == piloto_id)
    return session.exec(statement).all()
