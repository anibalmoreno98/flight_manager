from sqlmodel import Session
from fastapi import HTTPException

from app.models.piloto import Piloto
from app.repositories import piloto as piloto_repo


def create_piloto_service(piloto: Piloto, session: Session, repo=piloto_repo):
    return repo.add(session, piloto)


def get_piloto_service(piloto_id: int, session: Session, repo=piloto_repo):
    piloto = repo.get(session, piloto_id)
    if not piloto:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    return piloto


def list_pilotos_service(session: Session, repo=piloto_repo):
    return repo.list_all(session)


def update_piloto_service(piloto_id: int, piloto_data: Piloto, session: Session, repo=piloto_repo):
    piloto = repo.get(session, piloto_id)
    if not piloto:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")

    piloto.nombre = piloto_data.nombre
    piloto.apellido = piloto_data.apellido
    piloto.licencia = piloto_data.licencia

    return repo.update(session, piloto)


def delete_piloto_service(piloto_id: int, session: Session, repo=piloto_repo):
    piloto = repo.get(session, piloto_id)
    if not piloto:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")

    repo.delete(session, piloto)
    return {"ok": True}
