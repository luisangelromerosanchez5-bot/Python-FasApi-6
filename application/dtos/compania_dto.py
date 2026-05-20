import re
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

class EmpleadoSinCompaniaDTO(BaseModel):
    nombre: str
    apellido: str
    correo: str
    cargo: str
    salario: float = Field(gt=0)

    @field_validator("correo")
    @classmethod
    def validate_correo(cls, v: str) -> str:
        regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(regex, v):
            raise ValueError("Formato de correo electrónico no válido")
        return v

    model_config = ConfigDict(from_attributes=True)

class CompaniaCreateDTO(BaseModel):
    nombre: str
    direccion: str
    telefono: str

class CompaniaUpdateDTO(BaseModel):
    nombre: str | None = None
    direccion: str | None = None
    telefono: str | None = None

class CompaniaResponseDTO(BaseModel):
    id: int
    nombre: str
    direccion: str
    telefono: str
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)

class CompaniaConEmpleadosCreateDTO(BaseModel):
    nombre: str
    direccion: str
    telefono: str
    empleados: list[EmpleadoSinCompaniaDTO]
