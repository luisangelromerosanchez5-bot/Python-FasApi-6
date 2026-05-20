import logging

# Configurar el logging de forma global al inicio del archivo
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", encoding="utf-8")
    ]
)

logger = logging.getLogger(__name__)

from fastapi import FastAPI
from domain.entities import Base
# Importaciones necesarias para registrar los modelos en Base.metadata
from domain.entities.compania import Compania
from domain.entities.empleado import Empleado
from infrastructure.database.connection import engine, SessionLocal
from infrastructure.database.seed_data import seed_data
from api.controllers.companias_controller import router as companias_router
from api.controllers.empleados_controller import router as empleados_router
from api.middlewares.error_handler import register_error_handlers

app = FastAPI(
    title="API Compañías y Empleados",
    description="API REST con Onion Architecture + Repository Pattern + Unit of Work",
    version="1.0.0"
)

# Registrar middlewares / manejadores de errores
register_error_handlers(app)

# Registrar controladores
app.include_router(companias_router)
app.include_router(empleados_router)

@app.on_event("startup")
def startup():
    logger.info("Iniciando aplicación...")
    try:
        # Generar las tablas en la base de datos si no existen
        Base.metadata.create_all(bind=engine)
        logger.info("Esquemas de base de datos creados o verificados.")
        
        # Ejecutar el sembrado de datos (seeding)
        with SessionLocal() as db:
            seed_data(db)
        logger.info("Sembrado de datos finalizado.")
    except Exception as e:
        logger.error(f"Error durante la inicialización del startup: {str(e)}", exc_info=True)
    logger.info("Aplicación lista.")
