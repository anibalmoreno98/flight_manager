from typing import List
from sqlmodel import Session, select
from app.models.mision import Mision

class MisionRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(self, mision: Mision) -> Mision:
        self.session.add(mision)
        self.session.commit()
        self.session.refresh(mision)
        return mision

    def get(self, mision_id: int) -> Mision | None:
        return self.session.get(Mision, mision_id)

    def list_all(self) -> List[Mision]:
        return self.session.exec(select(Mision)).all()

    def update(self, mision: Mision) -> Mision:
        self.session.add(mision)
        self.session.commit()
        self.session.refresh(mision)
        return mision

    def delete(self, mision: Mision) -> None:
        self.session.delete(mision)
        self.session.commit()
