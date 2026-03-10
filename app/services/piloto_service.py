from sqlmodel import Session
from fastapi import HTTPException

from app.models.piloto import Piloto
from app.repositories import piloto as piloto_repo


def create_piloto_service(piloto: Piloto, session: Session, repo=piloto_repo):
    repo_instance = repo.PilotoRepository(session)
    return repo_instance.add(piloto)


def get_piloto_service(piloto_id: int, session: Session, repo=piloto_repo):
    repo_instance = repo.PilotoRepository(session)
    piloto = repo_instance.get(piloto_id)
    if not piloto:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    return piloto


def list_pilotos_service(session: Session, repo=piloto_repo):
    repo_instance = repo.PilotoRepository(session)
    return repo_instance.list_all()


def update_piloto_service(piloto_id: int, piloto_data: Piloto, session: Session, repo=piloto_repo):
    repo_instance = repo.PilotoRepository(session)
    piloto = repo_instance.get(piloto_id)
    if not piloto:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")

    piloto.nombre = piloto_data.nombre
    piloto.apellido = piloto_data.apellido
    piloto.licencia = piloto_data.licencia

    return repo_instance.update(piloto)


def delete_piloto_service(piloto_id: int, session: Session, repo=piloto_repo):
    repo_instance = repo.PilotoRepository(session)
    piloto = repo_instance.get(piloto_id)
    if not piloto:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")

    repo_instance.delete(piloto)
    return {"ok": True}
