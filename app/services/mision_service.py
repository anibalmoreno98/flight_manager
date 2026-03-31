from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.mision import Mision, EstadoMision
from app.models.piloto import Piloto
from app.models.aeronave import Aeronave
from app.models.usuario import Usuario
from app.models.vuelo import Vuelo
from app.repositories.mision import MisionRepository

class MisionService:

    def __init__(self, session: Session):
        self.session = session
        self.repo = MisionRepository(session)

    # -------------------------
    # VALIDACIONES INTERNAS
    # -------------------------

    def _validar_estado_editable(self, mision: Mision):
        if mision.estado in [EstadoMision.FINALIZADA, EstadoMision.CANCELADA]:
            raise HTTPException(400, "No se puede modificar una misión finalizada o cancelada.")

    def _validar_estado_eliminable(self, mision: Mision):
        if mision.estado in [EstadoMision.EN_CURSO, EstadoMision.FINALIZADA]:
            raise HTTPException(400, "No se puede eliminar una misión en curso o finalizada.")

    def _validar_piloto_disponible(self, piloto_id: int):
        misiones = self.session.exec(
            select(Mision).where(
                Mision.piloto_id == piloto_id,
                Mision.estado.in_([
                    EstadoMision.CREADA,
                    EstadoMision.PLANIFICADA,
                    EstadoMision.EN_CURSO
                ])
            )
        ).all()

        if misiones:
            raise HTTPException(400, "El piloto ya tiene una misión activa.")

    def _validar_aeronave_disponible(self, aeronave_id: int):
        aeronave = self.session.get(Aeronave, aeronave_id)
        if not aeronave:
            raise HTTPException(404, "Aeronave no encontrada")
        if aeronave.en_mantenimiento:
            raise HTTPException(400, "La aeronave está en mantenimiento.")

    def _validar_transicion_estado(self, estado_actual: EstadoMision, nuevo_estado: EstadoMision):
        orden = {
            EstadoMision.CREADA: 1,
            EstadoMision.PLANIFICADA: 2,
            EstadoMision.EN_CURSO: 3,
            EstadoMision.FINALIZADA: 4,
            EstadoMision.CANCELADA: 5
        }

        if orden[nuevo_estado] < orden[estado_actual]:
            raise HTTPException(400, "No se puede retroceder en el flujo de estados.")

    # -------------------------
    # MÉTODOS PÚBLICOS
    # -------------------------

    def create_mision_service(self, mision: Mision) -> Mision:
        usuario = self.session.get(Usuario, mision.creado_por)
        if not usuario:
            raise HTTPException(404, "Usuario creador no encontrado")

        if mision.piloto_id:
            self._validar_piloto_disponible(mision.piloto_id)

        if mision.aeronave_id:
            self._validar_aeronave_disponible(mision.aeronave_id)

        return self.repo.add(mision)

    def get_mision_service(self, mision_id: int) -> Mision:
        mision = self.repo.get(mision_id)
        if not mision:
            raise HTTPException(404, "Misión no encontrada")
        return mision

    def list_misiones_service(self) -> list[Mision]:
        return self.repo.list_all()

    def update_mision_service(self, mision_id: int, data: Mision) -> Mision:
        mision = self.get_mision_service(mision_id)

        self._validar_estado_editable(mision)

        if data.estado != mision.estado:
            self._validar_transicion_estado(mision.estado, data.estado)

        if data.piloto_id:
            self._validar_piloto_disponible(data.piloto_id)

        if data.aeronave_id:
            self._validar_aeronave_disponible(data.aeronave_id)

        mision.nombre = data.nombre
        mision.descripcion = data.descripcion
        mision.fecha_inicio = data.fecha_inicio
        mision.fecha_fin = data.fecha_fin
        mision.estado = data.estado
        mision.piloto_id = data.piloto_id
        mision.aeronave_id = data.aeronave_id

        return self.repo.update(mision)

    def delete_mision_service(self, mision_id: int) -> dict[str, bool]:
        mision = self.get_mision_service(mision_id)

        self._validar_estado_eliminable(mision)

        self.repo.delete(mision)
        return {"ok": True}
