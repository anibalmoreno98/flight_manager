from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.aeronave import Aeronave
from app.models.mision import Mision, EstadoMision
from app.models.vuelo import Vuelo
from app.repositories.aeronave import AeronaveRepository

class AeronaveService:

    def __init__(self, session: Session):
        self.session = session
        self.repo = AeronaveRepository(session)

    # -------------------------
    # VALIDACIONES INTERNAS
    # -------------------------

    def _validar_aeronave_no_asociada(self, aeronave_id: int):
        misiones = self.session.exec(
            select(Mision).where(Mision.aeronave_id == aeronave_id)
        ).all()

        vuelos = self.session.exec(
            select(Vuelo).where(Vuelo.aeronave_id == aeronave_id)
        ).all()

        if misiones or vuelos:
            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar una aeronave con misiones o vuelos asociados."
            )

    # -------------------------
    # MÉTODOS PÚBLICOS
    # -------------------------

    def create_aeronave_service(self, aeronave: Aeronave) -> Aeronave:
        return self.repo.add(aeronave)

    def get_aeronave_service(self, aeronave_id: int) -> Aeronave:
        aeronave = self.repo.get(aeronave_id)
        if not aeronave:
            raise HTTPException(404, "Aeronave no encontrada")
        return aeronave

    def list_aeronaves_service(self) -> list[Aeronave]:
        return self.repo.list_all()

    def update_aeronave_service(self, aeronave_id: int, data: Aeronave) -> Aeronave:
        aeronave = self.get_aeronave_service(aeronave_id)

        aeronave.fabricante = data.fabricante
        aeronave.modelo = data.modelo
        aeronave.numero_serie = data.numero_serie
        aeronave.velocidad_maxima = data.velocidad_maxima
        aeronave.en_mantenimiento = data.en_mantenimiento

        return self.repo.update(aeronave)

    def delete_aeronave_service(self, aeronave_id: int) -> dict[str, bool]:
        aeronave = self.get_aeronave_service(aeronave_id)

        self._validar_aeronave_no_asociada(aeronave_id)

        self.repo.delete(aeronave)
        return {"ok": True}
