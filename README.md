# API REST — Onion Architecture (Python + FastAPI + SQLAlchemy + SQL Server)

Este proyecto implementa una API REST completa en Python siguiendo la **Arquitectura Onion** (Arquitectura de Cebolla) y el patrón **Repository & Unit of Work**.

## Estructura del Proyecto

```
proyecto/
├── domain/                  # Capa de Dominio (Núcleo)
│   ├── entities/            # Entidades de negocio (SQLAlchemy Mappings)
│   └── interfaces/          # Contratos / Repositorios y Unit of Work
├── application/             # Capa de Aplicación
│   ├── services/            # Lógica de aplicación y orquestación
│   └── dtos/                # Validaciones y transferencia de datos (Pydantic v2)
├── infrastructure/          # Capa de Infraestructura
│   ├── database/            # Conexión a la BD y Seeding de datos
│   ├── repositories/        # Implementaciones de repositorios
│   └── unit_of_work/        # Implementación de Unit of Work (Context Manager)
├── api/                     # Capa de Entrada / API
│   ├── controllers/         # Controladores / Endpoints
│   ├── middlewares/         # Middleware global para manejo de errores
│   └── main.py              # Punto de entrada de FastAPI
├── alembic/                 # Migraciones de base de datos
├── alembic.ini
├── .env                     # Variables de entorno
├── requirements.txt         # Dependencias
└── README.md
```

## Requisitos de Instalación

1. Crear un entorno virtual e instalar las dependencias:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # En Windows
   pip install -r requirements.txt
   ```

2. Configurar el archivo `.env` con las credenciales de tu base de datos SQL Server.

3. Ejecutar las migraciones de Alembic (opcional, ya que en el startup se autogenera la base de datos si no existe):
   ```bash
   alembic upgrade head
   ```

4. Ejecutar el servidor:
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

5. Acceder a la documentación interactiva (Swagger) en: `http://localhost:8000/docs`.
