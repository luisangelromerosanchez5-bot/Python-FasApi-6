import logging
from domain.interfaces.unit_of_work import IUnitOfWork
from infrastructure.database.connection import SessionLocal
from infrastructure.repositories.compania_repository_impl import CompaniaRepositoryImpl
from infrastructure.repositories.empleado_repository_impl import EmpleadoRepositoryImpl

logger = logging.getLogger(__name__)

class UnitOfWorkImpl(IUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session = None
        self._companias = None
        self._empleados = None

    def __enter__(self):
        self._session = self.session_factory()
        self._companias = CompaniaRepositoryImpl(self._session)
        self._empleados = EmpleadoRepositoryImpl(self._session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                logger.error(f"Error en transacción: {exc_val}. Haciendo rollback.")
                self.rollback()
        finally:
            if self._session:
                self._session.close()

    @property
    def companias(self) -> CompaniaRepositoryImpl:
        return self._companias

    @property
    def empleados(self) -> EmpleadoRepositoryImpl:
        return self._empleados

    def commit(self) -> None:
        logger.info("Confirmando transacción (commit).")
        if self._session:
            self._session.commit()

    def rollback(self) -> None:
        logger.warning("Revirtiendo transacción (rollback).")
        if self._session:
            self._session.rollback()

    def save_changes(self) -> None:
        self.commit()

def get_uow() -> IUnitOfWork:
    """Función proveedora de Unit of Work para la inyección de dependencias de FastAPI."""
    return UnitOfWorkImpl(session_factory=SessionLocal)
