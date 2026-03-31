from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.piloto import Piloto
from app.models.mision import Mision, EstadoMision
from app.models.vuelo import Vuelo
from app.repositories.piloto import PilotoRepository

class PilotoService:

    def __init__(self, session: Session):
        self.session = session
        self.repo = PilotoRepository(session)

    # -------------------------
    # VALIDACIONES INTERNAS
    # -------------------------

    def _validar_piloto_disponible(self, piloto_id: int):
        misiones_activas = self.session.exec(
            select(Mision).where(
                Mision.piloto_id == piloto_id,
                Mision.estado.in_([
                    EstadoMision.CREADA,
                    EstadoMision.PLANIFICADA,
                    EstadoMision.EN_CURSO
                ])
            )
        ).all()

        if misiones_activas:
            raise HTTPException(
                400,
                "El piloto ya tiene una misión activa."
            )

    def _validar_piloto_no_asociado(self, piloto_id: int):
        misiones = self.session.exec(
            select(Mision).where(Mision.piloto_id == piloto_id)
        ).all()

        vuelos = self.session.exec(
            select(Vuelo).where(Vuelo.piloto_id == piloto_id)
        ).all()

        if misiones or vuelos:
            raise HTTPException(
                400,
                "No se puede eliminar un piloto con misiones o vuelos asociados."
            )

    # -------------------------
    # MÉTODOS PÚBLICOS
    # -------------------------

    def create_piloto_service(self, piloto: Piloto) -> Piloto:
        return self.repo.add(piloto)

    def get_piloto_service(self, piloto_id: int) -> Piloto:
        piloto = self.repo.get(piloto_id)
        if not piloto:
            raise HTTPException(404, "Piloto no encontrado")
        return piloto

    def list_pilotos_service(self) -> list[Piloto]:
        return self.repo.list_all()

    def update_piloto_service(self, piloto_id: int, data: Piloto) -> Piloto:
        piloto = self.get_piloto_service(piloto_id)

        piloto.nombre = data.nombre
        piloto.apellido = data.apellido
        piloto.licencia = data.licencia

        return self.repo.update(piloto)

    def delete_piloto_service(self, piloto_id: int) -> dict[str, bool]:
        piloto = self.get_piloto_service(piloto_id)
        self._validar_piloto_no_asociado(piloto_id)

        self.repo.delete(piloto)
        return {"ok": True}
