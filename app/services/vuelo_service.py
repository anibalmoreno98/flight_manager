from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.vuelo import Vuelo
from app.models.mision import Mision, EstadoMision
from app.models.piloto import Piloto
from app.models.aeronave import Aeronave
from app.models.telemetria import Telemetria
from app.repositories.vuelo import VueloRepository

class VueloService:

    def __init__(self, session: Session):
        self.session = session
        self.repo = VueloRepository(session)

    # -------------------------
    # VALIDACIONES INTERNAS
    # -------------------------

    def _validar_mision_activa(self, mision_id: int):
        mision = self.session.get(Mision, mision_id)
        if not mision:
            raise HTTPException(404, "Misión no encontrada")

        if mision.estado in [EstadoMision.FINALIZADA, EstadoMision.CANCELADA]:
            raise HTTPException(400, "No se pueden crear o modificar vuelos en una misión finalizada o cancelada.")

    def _validar_vuelo_sin_telemetria(self, vuelo_id: int):
        tele = self.session.exec(
            select(Telemetria).where(Telemetria.vuelo_id == vuelo_id)
        ).all()

        if tele:
            raise HTTPException(400, "No se puede eliminar un vuelo con telemetría asociada.")

    # -------------------------
    # MÉTODOS PÚBLICOS
    # -------------------------

    def create_vuelo_service(self, vuelo: Vuelo) -> Vuelo:
        piloto = self.session.get(Piloto, vuelo.piloto_id)
        if not piloto:
            raise HTTPException(404, "Piloto no encontrado")

        aeronave = self.session.get(Aeronave, vuelo.aeronave_id)
        if not aeronave:
            raise HTTPException(404, "Aeronave no encontrada")

        self._validar_mision_activa(vuelo.mision_id)

        return self.repo.add(vuelo)

    def get_vuelo_service(self, vuelo_id: int) -> Vuelo:
        vuelo = self.repo.get(vuelo_id)
        if not vuelo:
            raise HTTPException(404, "Vuelo no encontrado")
        return vuelo

    def list_vuelos_service(self) -> list[Vuelo]:
        return self.repo.list_all()

    def update_vuelo_service(self, vuelo_id: int, data: Vuelo) -> Vuelo:
        vuelo = self.get_vuelo_service(vuelo_id)

        self._validar_mision_activa(vuelo.mision_id)

        piloto = self.session.get(Piloto, data.piloto_id)
        if not piloto:
            raise HTTPException(404, "Piloto no encontrado")

        aeronave = self.session.get(Aeronave, data.aeronave_id)
        if not aeronave:
            raise HTTPException(404, "Aeronave no encontrada")

        vuelo.fecha_inicio = data.fecha_inicio
        vuelo.fecha_fin = data.fecha_fin
        vuelo.piloto_id = data.piloto_id
        vuelo.aeronave_id = data.aeronave_id

        return self.repo.update(vuelo)

    def delete_vuelo_service(self, vuelo_id: int) -> dict[str, bool]:
        vuelo = self.get_vuelo_service(vuelo_id)
        self._validar_vuelo_sin_telemetria(vuelo_id)

        self.repo.delete(vuelo)
        return {"ok": True}
