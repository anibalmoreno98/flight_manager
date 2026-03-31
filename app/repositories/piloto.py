from typing import List
from sqlmodel import Session, select
from app.models.piloto import Piloto

class PilotoRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(self, piloto: Piloto) -> Piloto:
        self.session.add(piloto)
        self.session.commit()
        self.session.refresh(piloto)
        return piloto

    def get(self, piloto_id: int) -> Piloto | None:
        return self.session.get(Piloto, piloto_id)

    def list_all(self) -> List[Piloto]:
        return self.session.exec(select(Piloto)).all()

    def update(self, piloto: Piloto) -> Piloto:
        self.session.add(piloto)
        self.session.commit()
        self.session.refresh(piloto)
        return piloto

    def delete(self, piloto: Piloto) -> None:
        self.session.delete(piloto)
        self.session.commit()
