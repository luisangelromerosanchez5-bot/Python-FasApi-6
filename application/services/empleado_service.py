import logging
from fastapi import HTTPException
from domain.interfaces.unit_of_work import IUnitOfWork
from domain.entities.empleado import Empleado
from application.dtos.empleado_dto import (
    EmpleadoCreateDTO,
    EmpleadoUpdateDTO,
    EmpleadoResponseDTO
)

logger = logging.getLogger(__name__)

class EmpleadoService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def get_all(self) -> list[EmpleadoResponseDTO]:
        logger.info("Obteniendo todos los empleados.")
        try:
            with self.uow:
                empleados = self.uow.empleados.get_all()
                result = [EmpleadoResponseDTO.model_validate(e) for e in empleados]
                logger.info(f"Se obtuvieron {len(result)} empleados con éxito.")
                return result
        except Exception as e:
            logger.error(f"Error al obtener empleados: {str(e)}")
            raise

    def get_by_id(self, id: int) -> EmpleadoResponseDTO:
        logger.info(f"Buscando empleado con ID: {id}.")
        with self.uow:
            empleado = self.uow.empleados.get_by_id(id)
            if not empleado:
                logger.warning(f"Recurso no encontrado: Empleado con ID {id} no existe.")
                raise HTTPException(status_code=404, detail=f"Empleado con ID {id} no encontrado")
            logger.info(f"Empleado con ID {id} encontrado con éxito.")
            return EmpleadoResponseDTO.model_validate(empleado)

    def get_by_compania(self, compania_id: int) -> list[EmpleadoResponseDTO]:
        logger.info(f"Buscando empleados de la compañía con ID: {compania_id}.")
        with self.uow:
            # Primero validamos que la compañía exista
            compania = self.uow.companias.get_by_id(compania_id)
            if not compania:
                logger.warning(f"Recurso no encontrado: Compañía con ID {compania_id} no existe.")
                raise HTTPException(status_code=404, detail=f"Compañía con ID {compania_id} no encontrada")
            
            empleados = self.uow.empleados.get_by_compania(compania_id)
            result = [EmpleadoResponseDTO.model_validate(e) for e in empleados]
            logger.info(f"Se obtuvieron {len(result)} empleados para la compañía con ID {compania_id} con éxito.")
            return result

    def create(self, dto: EmpleadoCreateDTO) -> EmpleadoResponseDTO:
        logger.info(f"Iniciando creación de empleado: {dto.nombre} {dto.apellido}.")
        try:
            with self.uow:
                # Validar existencia de la compañía
                compania = self.uow.companias.get_by_id(dto.compania_id)
                if not compania:
                    logger.warning(f"Recurso no encontrado: Compañía con ID {dto.compania_id} no existe. No se puede crear empleado.")
                    raise HTTPException(status_code=404, detail="Compañía no encontrada")
                
                # Validar correo único si es necesario
                # (aunque la BD lo restringirá, Onion lo valida en app/dominio antes de insertar)
                existing = self.uow.empleados.find_by_condition(Empleado.correo == dto.correo)
                if existing:
                    logger.warning(f"Conflicto de negocio: El correo {dto.correo} ya está registrado.")
                    raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

                empleado = Empleado(
                    nombre=dto.nombre,
                    apellido=dto.apellido,
                    correo=dto.correo,
                    cargo=dto.cargo,
                    salario=dto.salario,
                    compania_id=dto.compania_id
                )
                self.uow.empleados.create(empleado)
                self.uow.commit()
                logger.info(f"Empleado {dto.nombre} creado con éxito con ID {empleado.id}.")
                return EmpleadoResponseDTO.model_validate(empleado)
        except Exception as e:
            logger.error(f"Error al crear empleado {dto.nombre}: {str(e)}")
            raise

    def update(self, id: int, dto: EmpleadoUpdateDTO) -> EmpleadoResponseDTO:
        logger.info(f"Iniciando actualización de empleado con ID: {id}.")
        try:
            with self.uow:
                empleado = self.uow.empleados.get_by_id(id)
                if not empleado:
                    logger.warning(f"Recurso no encontrado: Empleado con ID {id} no existe para actualizar.")
                    raise HTTPException(status_code=404, detail=f"Empleado con ID {id} no encontrado")
                
                if dto.nombre is not None:
                    empleado.nombre = dto.nombre
                if dto.apellido is not None:
                    empleado.apellido = dto.apellido
                if dto.cargo is not None:
                    empleado.cargo = dto.cargo
                if dto.salario is not None:
                    empleado.salario = dto.salario
                
                if dto.correo is not None and dto.correo != empleado.correo:
                    # Validar correo único
                    existing = self.uow.empleados.find_by_condition(Empleado.correo == dto.correo)
                    if existing:
                        logger.warning(f"Conflicto de negocio: El correo {dto.correo} ya está registrado.")
                        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
                    empleado.correo = dto.correo
                
                self.uow.empleados.update(empleado)
                self.uow.commit()
                logger.info(f"Empleado con ID {id} actualizado con éxito.")
                return EmpleadoResponseDTO.model_validate(empleado)
        except Exception as e:
            logger.error(f"Error al actualizar empleado con ID {id}: {str(e)}")
            raise

    def delete(self, id: int) -> None:
        logger.info(f"Iniciando eliminación de empleado con ID: {id}.")
        try:
            with self.uow:
                empleado = self.uow.empleados.get_by_id(id)
                if not empleado:
                    logger.warning(f"Recurso no encontrado: Empleado con ID {id} no existe para eliminar.")
                    raise HTTPException(status_code=404, detail=f"Empleado con ID {id} no encontrado")
                
                self.uow.empleados.delete(empleado)
                self.uow.commit()
                logger.info(f"Empleado con ID {id} eliminado con éxito.")
        except Exception as e:
            logger.error(f"Error al eliminar empleado con ID {id}: {str(e)}")
            raise
