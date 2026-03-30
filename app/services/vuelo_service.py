from sqlmodel import Session
from fastapi import HTTPException
from app.models.vuelo import Vuelo
from app.models.usuario import Usuario
from app.repositories.vuelo import VueloRepository

class VueloService:

    def __init__(self, session: Session):
        self.session = session
        self.repo = VueloRepository(session)

    def create_vuelo_service(self, vuelo: Vuelo) -> Vuelo:
        usuario = self.session.get(Usuario, vuelo.piloto)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario (piloto) no encontrado")

        return self.repo.add(vuelo)

    def get_vuelo_service(self, vuelo_id: int) -> Vuelo:
        vuelo = self.repo.get(vuelo_id)
        if not vuelo:
            raise HTTPException(status_code=404, detail="Vuelo no encontrado")
        return vuelo

    def list_vuelos_service(self) -> list[Vuelo]:
        return self.repo.list_all()

    def update_vuelo_service(self, vuelo_id: int, vuelo_data: Vuelo) -> Vuelo:
        vuelo = self.repo.get(vuelo_id)
        if not vuelo:
            raise HTTPException(status_code=404, detail="Vuelo no encontrado")

        vuelo.fecha_inicio = vuelo_data.fecha_inicio
        vuelo.fecha_fin = vuelo_data.fecha_fin
        vuelo.piloto = vuelo_data.piloto
        vuelo.aeronave = vuelo_data.aeronave
        vuelo.telemetria = vuelo_data.telemetria

        return self.repo.update(vuelo)

    def delete_vuelo_service(self, vuelo_id: int) -> dict[str, bool]:
        vuelo = self.repo.get(vuelo_id)
        if not vuelo:
            raise HTTPException(status_code=404, detail="Vuelo no encontrado")

        self.repo.delete(vuelo)
        return {"ok": True}
