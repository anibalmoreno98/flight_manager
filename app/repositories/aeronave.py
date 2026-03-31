from typing import List
from sqlmodel import Session, select
from app.models.aeronave import Aeronave

class AeronaveRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(self, aeronave: Aeronave) -> Aeronave:
        self.session.add(aeronave)
        self.session.commit()
        self.session.refresh(aeronave)
        return aeronave

    def get(self, aeronave_id: int) -> Aeronave | None:
        return self.session.get(Aeronave, aeronave_id)

    def list_all(self) -> List[Aeronave]:
        return self.session.exec(select(Aeronave)).all()

    def update(self, aeronave: Aeronave) -> Aeronave:
        self.session.add(aeronave)
        self.session.commit()
        self.session.refresh(aeronave)
        return aeronave

    def delete(self, aeronave: Aeronave) -> None:
        self.session.delete(aeronave)
        self.session.commit()
