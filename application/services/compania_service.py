import logging
from fastapi import HTTPException
from domain.interfaces.unit_of_work import IUnitOfWork
from domain.entities.compania import Compania
from domain.entities.empleado import Empleado
from application.dtos.compania_dto import (
    CompaniaCreateDTO,
    CompaniaUpdateDTO,
    CompaniaResponseDTO,
    CompaniaConEmpleadosCreateDTO
)

logger = logging.getLogger(__name__)

class CompaniaService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def get_all(self) -> list[CompaniaResponseDTO]:
        logger.info("Obteniendo todas las compañías.")
        try:
            with self.uow:
                companias = self.uow.companias.get_all()
                result = [CompaniaResponseDTO.model_validate(c) for c in companias]
                logger.info(f"Se obtuvieron {len(result)} compañías con éxito.")
                return result
        except Exception as e:
            logger.error(f"Error al obtener compañías: {str(e)}")
            raise

    def get_by_id(self, id: int) -> CompaniaResponseDTO:
        logger.info(f"Buscando compañía con ID: {id}.")
        with self.uow:
            compania = self.uow.companias.get_by_id(id)
            if not compania:
                logger.warning(f"Recurso no encontrado: Compañía con ID {id} no existe.")
                raise HTTPException(status_code=404, detail=f"Compañía con ID {id} no encontrada")
            logger.info(f"Compañía con ID {id} encontrada con éxito.")
            return CompaniaResponseDTO.model_validate(compania)

    def create(self, dto: CompaniaCreateDTO) -> CompaniaResponseDTO:
        logger.info(f"Iniciando creación de compañía: {dto.nombre}.")
        try:
            with self.uow:
                compania = Compania(
                    nombre=dto.nombre,
                    direccion=dto.direccion,
                    telefono=dto.telefono
                )
                self.uow.companias.create(compania)
                self.uow.commit()
                logger.info(f"Compañía {dto.nombre} creada con éxito con ID {compania.id}.")
                return CompaniaResponseDTO.model_validate(compania)
        except Exception as e:
            logger.error(f"Error al crear compañía {dto.nombre}: {str(e)}")
            raise

    def update(self, id: int, dto: CompaniaUpdateDTO) -> CompaniaResponseDTO:
        logger.info(f"Iniciando actualización de compañía con ID: {id}.")
        try:
            with self.uow:
                compania = self.uow.companias.get_by_id(id)
                if not compania:
                    logger.warning(f"Recurso no encontrado: Compañía con ID {id} no existe para actualizar.")
                    raise HTTPException(status_code=404, detail=f"Compañía con ID {id} no encontrada")
                
                if dto.nombre is not None:
                    compania.nombre = dto.nombre
                if dto.direccion is not None:
                    compania.direccion = dto.direccion
                if dto.telefono is not None:
                    compania.telefono = dto.telefono
                
                self.uow.companias.update(compania)
                self.uow.commit()
                logger.info(f"Compañía con ID {id} actualizada con éxito.")
                return CompaniaResponseDTO.model_validate(compania)
        except Exception as e:
            logger.error(f"Error al actualizar compañía con ID {id}: {str(e)}")
            raise

    def delete(self, id: int) -> None:
        logger.info(f"Iniciando eliminación de compañía con ID: {id}.")
        try:
            with self.uow:
                compania = self.uow.companias.get_by_id(id)
                if not compania:
                    logger.warning(f"Recurso no encontrado: Compañía con ID {id} no existe para eliminar.")
                    raise HTTPException(status_code=404, detail=f"Compañía con ID {id} no encontrada")
                
                self.uow.companias.delete(compania)
                self.uow.commit()
                logger.info(f"Compañía con ID {id} eliminada con éxito.")
        except Exception as e:
            logger.error(f"Error al eliminar compañía con ID {id}: {str(e)}")
            raise

    def get_con_empleados(self, id: int) -> dict:
        logger.info(f"Obteniendo compañía con ID: {id} y sus empleados.")
        with self.uow:
            compania = self.uow.companias.get_with_empleados(id)
            if not compania:
                logger.warning(f"Recurso no encontrado: Compañía con ID {id} no existe.")
                raise HTTPException(status_code=404, detail=f"Compañía con ID {id} no encontrada")
            
            result = {
                "id": compania.id,
                "nombre": compania.nombre,
                "direccion": compania.direccion,
                "telefono": compania.telefono,
                "fecha_creacion": compania.fecha_creacion,
                "empleados": [
                    {
                        "id": emp.id,
                        "nombre": emp.nombre,
                        "apellido": emp.apellido,
                        "correo": emp.correo,
                        "cargo": emp.cargo,
                        "salario": float(emp.salario),
                        "compania_id": emp.compania_id
                    } for emp in compania.empleados
                ]
            }
            logger.info(f"Compañía con ID {id} y sus {len(compania.empleados)} empleados obtenidos con éxito.")
            return result

    def create_con_empleados(self, dto: CompaniaConEmpleadosCreateDTO) -> CompaniaResponseDTO:
        logger.info("Inicio de transacción con empleados (create_con_empleados).")
        try:
            with self.uow:
                compania = Compania(
                    nombre=dto.nombre,
                    direccion=dto.direccion,
                    telefono=dto.telefono
                )
                self.uow.companias.create(compania)
                # Forzar la asignación de ID a la compañía agregándola
                # para que esté disponible en los empleados creados.
                # En SQLAlchemy, al agregarla y estar dentro de la misma sesión, 
                # la relación se puede manejar de forma automática
                # o pasándole la instancia de compania.
                
                for emp_dto in dto.empleados:
                    empleado = Empleado(
                        nombre=emp_dto.nombre,
                        apellido=emp_dto.apellido,
                        correo=emp_dto.correo,
                        cargo=emp_dto.cargo,
                        salario=emp_dto.salario,
                        compania=compania  # Asociar directamente al objeto compania recién creado
                    )
                    self.uow.empleados.create(empleado)
                
                self.uow.commit()
                logger.info(f"Compañía transaccional con empleados creada con éxito. ID Compañía: {compania.id}.")
                return CompaniaResponseDTO.model_validate(compania)
        except Exception as e:
            logger.error(f"Error en creación transaccional de compañía con empleados: {str(e)}")
            raise
