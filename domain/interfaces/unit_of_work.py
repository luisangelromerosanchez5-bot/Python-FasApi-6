from abc import ABC, abstractmethod
from domain.interfaces.compania_repository import ICompaniaRepository
from domain.interfaces.empleado_repository import IEmpleadoRepository

class IUnitOfWork(ABC):
    @property
    @abstractmethod
    def companias(self) -> ICompaniaRepository:
        """Repositorio de compañías."""
        pass

    @property
    @abstractmethod
    def empleados(self) -> IEmpleadoRepository:
        """Repositorio de empleados."""
        pass

    @abstractmethod
    def commit(self) -> None:
        """Confirma la transacción actual."""
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Revierte la transacción actual."""
        pass

    @abstractmethod
    def save_changes(self) -> None:
        """Alias de commit."""
        pass

    @abstractmethod
    def __enter__(self) -> "IUnitOfWork":
        """Inicia el administrador de contexto."""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Finaliza el administrador de contexto, revirtiendo si ocurre una excepción."""
        pass
