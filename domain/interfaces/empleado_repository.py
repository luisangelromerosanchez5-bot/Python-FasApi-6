from abc import ABC, abstractmethod
from typing import List, Any
from domain.entities.empleado import Empleado

class IEmpleadoRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Empleado]:
        """Obtiene todos los empleados."""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Empleado | None:
        """Obtiene un empleado por su ID."""
        pass

    @abstractmethod
    def get_by_compania(self, compania_id: int) -> List[Empleado]:
        """Obtiene todos los empleados que pertenecen a una compañía específica."""
        pass

    @abstractmethod
    def create(self, empleado: Empleado) -> None:
        """Crea un empleado. No realiza commit."""
        pass

    @abstractmethod
    def update(self, empleado: Empleado) -> None:
        """Actualiza un empleado. No realiza commit."""
        pass

    @abstractmethod
    def delete(self, empleado: Empleado) -> None:
        """Elimina un empleado. No realiza commit."""
        pass

    @abstractmethod
    def find_by_condition(self, condition: Any) -> List[Empleado]:
        """Busca empleados según una condición SQLAlchemy."""
        pass
