from abc import ABC, abstractmethod
from typing import List, Any
from domain.entities.compania import Compania

class ICompaniaRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Compania]:
        """Obtiene todas las compañías."""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Compania | None:
        """Obtiene una compañía por su ID."""
        pass

    @abstractmethod
    def create(self, compania: Compania) -> None:
        """Crea una compañía. No realiza commit."""
        pass

    @abstractmethod
    def update(self, compania: Compania) -> None:
        """Actualiza una compañía. No realiza commit."""
        pass

    @abstractmethod
    def delete(self, compania: Compania) -> None:
        """Elimina una compañía. No realiza commit."""
        pass

    @abstractmethod
    def find_by_condition(self, condition: Any) -> List[Compania]:
        """Busca compañías según una condición SQLAlchemy."""
        pass

    @abstractmethod
    def get_with_empleados(self, id: int) -> Compania | None:
        """Obtiene una compañía con sus empleados cargados en una sola consulta."""
        pass
