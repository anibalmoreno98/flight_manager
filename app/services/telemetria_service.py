from sqlmodel import Session
from fastapi import HTTPException

from app.models.telemetria import Telemetria
from app.repositories.telemetria import TelemetriaRepository

class   TelemetriaService:

    def __init__(self, session: Session):
        self.session = session
        self.repo = TelemetriaRepository(session)

    def create_telemetria_service(self, telemetria: Telemetria) -> Telemetria:
        return self.repo.add(telemetria)


    def get_telemetria_service(self, telemetria_id: int) -> Telemetria:
        tele = self.repo.get(telemetria_id)
        if not tele:
            raise HTTPException(status_code=404, detail="Telemetria no encontrada")
        return tele


    def list_telemetria_service(self) -> list[Telemetria]:
        return self.repo.list_all()


    def update_telemetria_service(self, telemetria_id: int, telemetria_data: Telemetria) -> Telemetria:
        tele = self.repo.get(telemetria_id)
        if not tele:
            raise HTTPException(status_code=404, detail="Telemetria no encontrada")

        tele.altura_maxima = telemetria_data.altura_maxima
        tele.velocidad_maxima = telemetria_data.velocidad_maxima

        return self.repo.update(self.session, tele)


    def delete_telemetria_service(self, telemetria_id: int) -> dict[str, bool]:
        tele = self.repo.get(telemetria_id)
        if not tele:
            raise HTTPException(status_code=404, detail="Telemetria no encontrada")

        self.repo.delete(tele)
        return {"ok": True}