from fastapi import APIRouter, Depends, status, Response
from domain.interfaces.unit_of_work import IUnitOfWork
from infrastructure.unit_of_work.unit_of_work_impl import get_uow
from application.services.empleado_service import EmpleadoService
from application.dtos.empleado_dto import (
    EmpleadoCreateDTO,
    EmpleadoUpdateDTO,
    EmpleadoResponseDTO
)

router = APIRouter(prefix="/api/empleados", tags=["Empleados"])

@router.get("", response_model=list[EmpleadoResponseDTO])
def get_all(uow: IUnitOfWork = Depends(get_uow)):
    service = EmpleadoService(uow)
    return service.get_all()

@router.get("/{id}", response_model=EmpleadoResponseDTO)
def get_by_id(id: int, uow: IUnitOfWork = Depends(get_uow)):
    service = EmpleadoService(uow)
    return service.get_by_id(id)

@router.post("", response_model=EmpleadoResponseDTO, status_code=status.HTTP_201_CREATED)
def create(dto: EmpleadoCreateDTO, uow: IUnitOfWork = Depends(get_uow)):
    service = EmpleadoService(uow)
    return service.create(dto)

@router.put("/{id}", response_model=EmpleadoResponseDTO)
def update(id: int, dto: EmpleadoUpdateDTO, uow: IUnitOfWork = Depends(get_uow)):
    service = EmpleadoService(uow)
    return service.update(id, dto)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, uow: IUnitOfWork = Depends(get_uow)):
    service = EmpleadoService(uow)
    service.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
