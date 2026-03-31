from typing import List
from sqlmodel import Session, select
from app.models.telemetria import Telemetria

class TelemetriaRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(self, tele: Telemetria) -> Telemetria:
        self.session.add(tele)
        self.session.commit()
        self.session.refresh(tele)
        return tele

    def get(self, telemetria_id: int) -> Telemetria | None:
        return self.session.get(Telemetria, telemetria_id)

    def list_all(self) -> List[Telemetria]:
        return self.session.exec(select(Telemetria)).all()

    def update(self, tele: Telemetria) -> Telemetria:
        self.session.add(tele)
        self.session.commit()
        self.session.refresh(tele)
        return tele

    def delete(self, tele: Telemetria) -> None:
        self.session.delete(tele)
        self.session.commit()
