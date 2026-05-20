from typing import List, Any
from sqlalchemy.orm import Session, joinedload
from domain.entities.compania import Compania
from domain.interfaces.compania_repository import ICompaniaRepository

class CompaniaRepositoryImpl(ICompaniaRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Compania]:
        return self.session.query(Compania).all()

    def get_by_id(self, id: int) -> Compania | None:
        return self.session.query(Compania).filter(Compania.id == id).first()

    def create(self, compania: Compania) -> None:
        self.session.add(compania)

    def update(self, compania: Compania) -> None:
        self.session.merge(compania)

    def delete(self, compania: Compania) -> None:
        self.session.delete(compania)

    def find_by_condition(self, condition: Any) -> List[Compania]:
        return self.session.query(Compania).filter(condition).all()

    def get_with_empleados(self, id: int) -> Compania | None:
        return (
            self.session.query(Compania)
            .options(joinedload(Compania.empleados))
            .filter(Compania.id == id)
            .first()
        )
