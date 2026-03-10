from typing import List
from sqlmodel import Session, select

from app.models.vuelo import Vuelo

class VueloRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, vuelo: Vuelo) -> Vuelo:
        self.session.add(vuelo)
        self.session.commit()
        self.session.refresh(vuelo)
        return vuelo

    def get(self, vuelo_id: int) -> Vuelo | None:
        return self.session.get(Vuelo, vuelo_id)

    def list_all(self) -> List[Vuelo]:
        return self.session.exec(select(Vuelo)).all()

    def update(self, vuelo: Vuelo) -> Vuelo:
        self.session.add(vuelo)
        self.session.commit()
        self.session.refresh(vuelo)
        return vuelo

    def delete(self, vuelo: Vuelo) -> None:
        self.session.delete(vuelo)
        self.session.commit()

    # additional helpers

    def list_by_piloto(self, piloto_id: int) -> List[Vuelo]:
        statement = select(Vuelo).where(Vuelo.piloto == piloto_id)
        return self.session.exec(statement).all()
