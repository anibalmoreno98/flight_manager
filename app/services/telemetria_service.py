from sqlmodel import Session
from fastapi import HTTPException

from app.models.telemetria import Telemetria
from app.models.vuelo import Vuelo
from app.models.mision import Mision, EstadoMision
from app.repositories.telemetria import TelemetriaRepository

class TelemetriaService:

    def __init__(self, session: Session):
        self.session = session
        self.repo = TelemetriaRepository(session)

    def _validar_mision_activa(self, vuelo_id: int):
        vuelo = self.session.get(Vuelo, vuelo_id)
        if not vuelo:
            raise HTTPException(404, "Vuelo no encontrado")

        mision = self.session.get(Mision, vuelo.mision_id)
        if not mision:
            raise HTTPException(404, "Misión asociada no encontrada")

        if mision.estado in [EstadoMision.FINALIZADA, EstadoMision.CANCELADA]:
            raise HTTPException(400, "No se puede registrar telemetría en una misión finalizada o cancelada.")

    def create_telemetria_service(self, telemetria: Telemetria) -> Telemetria:
        self._validar_mision_activa(telemetria.vuelo_id)
        return self.repo.add(telemetria)

    def get_telemetria_service(self, telemetria_id: int) -> Telemetria:
        tele = self.repo.get(telemetria_id)
        if not tele:
            raise HTTPException(404, "Telemetría no encontrada")
        return tele

    def list_telemetria_service(self) -> list[Telemetria]:
        return self.repo.list_all()

    def update_telemetria_service(self, telemetria_id: int, data: Telemetria) -> Telemetria:
        tele = self.get_telemetria_service(telemetria_id)
        self._validar_mision_activa(tele.vuelo_id)

        tele.altura_maxima = data.altura_maxima
        tele.velocidad_maxima = data.velocidad_maxima

        return self.repo.update(tele)

    def delete_telemetria_service(self, telemetria_id: int) -> dict[str, bool]:
        tele = self.get_telemetria_service(telemetria_id)
        self.repo.delete(tele)
        return {"ok": True}
