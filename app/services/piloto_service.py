from sqlmodel import Session
from fastapi import HTTPException

from app.models.piloto import Piloto
from app.repositories.piloto import PilotoRepository

class PilotoService:

    def __init__(self, session: Session):
        self.session = session
        self.repo = PilotoRepository(session)

    def create_piloto_service(self, piloto: Piloto) -> Piloto:
        return self.repo.add(self.session, piloto)


    def get_piloto_service(self, piloto_id: int) -> Piloto:
        piloto = self.repo.get(self.session, piloto_id)
        if not piloto:
            raise HTTPException(status_code=404, detail="Piloto no encontrado")
        return piloto


    def list_pilotos_service(self) -> list[Piloto]:
        return self.repo.list_all(self.session)


    def update_piloto_service(self, piloto_id: int, piloto_data: Piloto) -> Piloto:
        piloto = self.repo.get(self.session, piloto_id)
        if not piloto:
            raise HTTPException(status_code=404, detail="Piloto no encontrado")

        piloto.nombre = piloto_data.nombre
        piloto.apellido = piloto_data.apellido
        piloto.licencia = piloto_data.licencia

        return self.repo.update(self.session, piloto)


    def delete_piloto_service(self, piloto_id: int) -> dict[str, bool]:
        piloto = self.repo.get(self.session, piloto_id)
        if not piloto:
            raise HTTPException(status_code=404, detail="Piloto no encontrado")

        self.repo.delete(self.session, piloto)
        return {"ok": True}

    def delete_piloto_service(piloto_id: int, session: Session, repo=piloto_repo) -> dict[str, bool]:
        piloto = repo.get(session, piloto_id)
        if not piloto:
            raise HTTPException(status_code=404, detail="Piloto no encontrado")

        repo.delete(session, piloto)
        return {"ok": True}
