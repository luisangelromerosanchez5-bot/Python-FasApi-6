import re
from pydantic import BaseModel, ConfigDict, Field, field_validator

class EmpleadoCreateDTO(BaseModel):
    nombre: str
    apellido: str
    correo: str
    cargo: str
    salario: float = Field(gt=0)
    compania_id: int

    @field_validator("correo")
    @classmethod
    def validate_correo(cls, v: str) -> str:
        regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(regex, v):
            raise ValueError("Formato de correo electrónico no válido")
        return v

class EmpleadoUpdateDTO(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    correo: str | None = None
    cargo: str | None = None
    salario: float | None = Field(None, gt=0)

    @field_validator("correo")
    @classmethod
    def validate_correo(cls, v: str | None) -> str | None:
        if v is None:
            return v
        regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(regex, v):
            raise ValueError("Formato de correo electrónico no válido")
        return v

class EmpleadoResponseDTO(BaseModel):
    id: int
    nombre: str
    apellido: str
    correo: str
    cargo: str
    salario: float
    compania_id: int

    model_config = ConfigDict(from_attributes=True)
