from sqlmodel import Session
from fastapi import HTTPException

from app.models.mision import Mision
from app.models.usuario import Usuario
from app.repositories.mision import MisionRepository

class MisionService:

    def __init__(self, session: Session):
        self.session = session
        self.repo = MisionRepository(session)

    def create_mision_service(self, mision: Mision) -> Mision:
        usuario = self.session.get(Usuario, mision.creado_por)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return self.repo.add(self.session, mision)


    def get_mision_service(self, mision_id: int) -> Mision:
        mision = self.repo.get(self.session, mision_id)
        if not mision:
            raise HTTPException(status_code=404, detail="Mision no encontrada")
        return mision


    def list_misiones_service(self) -> list[Mision]:
        return self.repo.list_all(self.session)


    def update_mision_service(self, mision_id: int, mision_data: Mision) -> Mision:
        mision = self.repo.get(self.session, mision_id)
        if not mision:
            raise HTTPException(status_code=404, detail="Mision no encontrada")

        mision.nombre = mision_data.nombre
        mision.descripcion = mision_data.descripcion
        mision.fecha_inicio = mision_data.fecha_inicio
        mision.fecha_fin = mision_data.fecha_fin
        mision.creado_por = mision_data.creado_por

        return self.repo.update(self.session, mision)


    def delete_mision_service(self, mision_id: int) -> dict[str, bool]:
        mision = self.repo.get(self.session, mision_id)
        if not mision:
            raise HTTPException(status_code=404, detail="Mision no encontrada")

        self.repo.delete(self.session, mision)
        return {"ok": True}
