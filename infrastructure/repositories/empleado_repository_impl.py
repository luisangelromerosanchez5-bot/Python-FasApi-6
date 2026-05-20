from typing import List, Any
from sqlalchemy.orm import Session
from domain.entities.empleado import Empleado
from domain.interfaces.empleado_repository import IEmpleadoRepository

class EmpleadoRepositoryImpl(IEmpleadoRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Empleado]:
        return self.session.query(Empleado).all()

    def get_by_id(self, id: int) -> Empleado | None:
        return self.session.query(Empleado).filter(Empleado.id == id).first()

    def get_by_compania(self, compania_id: int) -> List[Empleado]:
        return self.session.query(Empleado).filter(Empleado.compania_id == compania_id).all()

    def create(self, empleado: Empleado) -> None:
        self.session.add(empleado)

    def update(self, empleado: Empleado) -> None:
        self.session.merge(empleado)

    def delete(self, empleado: Empleado) -> None:
        self.session.delete(empleado)

    def find_by_condition(self, condition: Any) -> List[Empleado]:
        return self.session.query(Empleado).filter(condition).all()
