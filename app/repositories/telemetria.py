from typing import List
from sqlmodel import Session, select

from app.models.telemetria import Telemetria

class TelemetriaRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, telemetria: Telemetria) -> Telemetria:
        self.session.add(telemetria)
        self.session.commit()
        self.session.refresh(telemetria)
        return telemetria

    def get(self, telemetria_id: int) -> Telemetria | None:
        return self.session.get(Telemetria, telemetria_id)

    def list_all(self) -> List[Telemetria]:
        return self.session.exec(select(Telemetria)).all()

    def update(self, telemetria: Telemetria) -> Telemetria:
        self.session.add(telemetria)
        self.session.commit()
        self.session.refresh(telemetria)
        return telemetria

    def delete(self, telemetria: Telemetria) -> None:
        self.session.delete(telemetria)
        self.session.commit()
