from fastapi import APIRouter, Depends, status, Response
from domain.interfaces.unit_of_work import IUnitOfWork
from infrastructure.unit_of_work.unit_of_work_impl import get_uow
from application.services.compania_service import CompaniaService
from application.services.empleado_service import EmpleadoService
from application.dtos.compania_dto import (
    CompaniaCreateDTO,
    CompaniaUpdateDTO,
    CompaniaResponseDTO,
    CompaniaConEmpleadosCreateDTO
)
from application.dtos.empleado_dto import EmpleadoResponseDTO

router = APIRouter(prefix="/api/companias", tags=["Compañías"])

@router.get("", response_model=list[CompaniaResponseDTO])
def get_all(uow: IUnitOfWork = Depends(get_uow)):
    service = CompaniaService(uow)
    return service.get_all()

@router.post("/con-empleados", response_model=CompaniaResponseDTO, status_code=status.HTTP_201_CREATED)
def create_con_empleados(dto: CompaniaConEmpleadosCreateDTO, uow: IUnitOfWork = Depends(get_uow)):
    service = CompaniaService(uow)
    return service.create_con_empleados(dto)

@router.get("/{id}", response_model=CompaniaResponseDTO)
def get_by_id(id: int, uow: IUnitOfWork = Depends(get_uow)):
    service = CompaniaService(uow)
    return service.get_by_id(id)

@router.post("", response_model=CompaniaResponseDTO, status_code=status.HTTP_201_CREATED)
def create(dto: CompaniaCreateDTO, uow: IUnitOfWork = Depends(get_uow)):
    service = CompaniaService(uow)
    return service.create(dto)

@router.put("/{id}", response_model=CompaniaResponseDTO)
def update(id: int, dto: CompaniaUpdateDTO, uow: IUnitOfWork = Depends(get_uow)):
    service = CompaniaService(uow)
    return service.update(id, dto)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, uow: IUnitOfWork = Depends(get_uow)):
    service = CompaniaService(uow)
    service.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{id}/empleados", response_model=list[EmpleadoResponseDTO])
def get_empleados(id: int, uow: IUnitOfWork = Depends(get_uow)):
    service = EmpleadoService(uow)
    return service.get_by_compania(id)
