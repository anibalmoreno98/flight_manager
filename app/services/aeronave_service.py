from sqlmodel import Session
from fastapi import HTTPException

from app.models.aeronave import Aeronave
from app.repositories.aeronave import AeronaveRepository

class AeronaveService:

    def __init__(self, session: Session):
        self.session = session
        self.repo = AeronaveRepository(session)

    def create_aeronave_service(self, aeronave: Aeronave) -> Aeronave:
        return self.repo.add(aeronave)


    def get_aeronave_service(self, aeronave_id: int) -> Aeronave:
        aeronave = self.repo.get(aeronave_id)
        if not aeronave:
            raise HTTPException(status_code=404, detail="Aeronave no encontrada")
        return aeronave


    def list_aeronaves_service(self) -> list[Aeronave]:
        return self.repo.list_all()


    def update_aeronave_service(self, aeronave_id: int, aeronave_data: Aeronave) -> Aeronave:
        aeronave = self.repo.get(aeronave_id)
        if not aeronave:
            raise HTTPException(status_code=404, detail="Aeronave no encontrada")

        aeronave.fabricante = aeronave_data.fabricante
        aeronave.modelo = aeronave_data.modelo
        aeronave.numero_serie = aeronave_data.numero_serie
        aeronave.velocidad_maxima = aeronave_data.velocidad_maxima

        return self.repo.update(aeronave)


    def delete_aeronave_service(self, aeronave_id: int) -> dict[str, bool]:
        aeronave = self.repo.get(aeronave_id)
        if not aeronave:
            raise HTTPException(status_code=404, detail="Aeronave no encontrada")

        self.repo.delete(aeronave)
        return {"ok": True}
