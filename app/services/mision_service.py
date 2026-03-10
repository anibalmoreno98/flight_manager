from sqlmodel import Session
from fastapi import HTTPException

from app.models.mision import Mision
from app.models.usuario import Usuario
from app.repositories import mision as mision_repo


def create_mision_service(mision: Mision, session: Session, repo=mision_repo):
    # validate creator exists
    usuario = session.get(Usuario, mision.creado_por)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    repo_instance = repo.MisionRepository(session)
    return repo_instance.add(mision)


def get_mision_service(mision_id: int, session: Session, repo=mision_repo):
    repo_instance = repo.MisionRepository(session)
    mision = repo_instance.get(mision_id)
    if not mision:
        raise HTTPException(status_code=404, detail="Mision no encontrada")
    return mision


def list_misiones_service(session: Session, repo=mision_repo):
    repo_instance = repo.MisionRepository(session)
    return repo_instance.list_all()


def update_mision_service(mision_id: int, mision_data: Mision, session: Session, repo=mision_repo):
    repo_instance = repo.MisionRepository(session)
    mision = repo_instance.get(mision_id)
    if not mision:
        raise HTTPException(status_code=404, detail="Mision no encontrada")

    mision.nombre = mision_data.nombre
    mision.descripcion = mision_data.descripcion
    mision.fecha_inicio = mision_data.fecha_inicio
    mision.fecha_fin = mision_data.fecha_fin
    mision.creado_por = mision_data.creado_por

    return repo_instance.update(mision)


def delete_mision_service(mision_id: int, session: Session, repo=mision_repo):
    repo_instance = repo.MisionRepository(session)
    mision = repo_instance.get(mision_id)
    if not mision:
        raise HTTPException(status_code=404, detail="Mision no encontrada")

    repo_instance.delete(mision)
    return {"ok": True}
