import os
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Cargar variables del archivo .env
load_dotenv()

DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_PORT = os.getenv("DB_PORT", "")  # Por defecto vacío para permitir instancias con nombre
DB_NAME = os.getenv("DB_NAME", "companias_db")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
DB_TRUSTED_CONNECTION = os.getenv("DB_TRUSTED_CONNECTION", "False").lower() in ("true", "1", "yes")

# SQL Server exige codificar el nombre del driver correctamente para SQLAlchemy.
driver_normalized = DB_DRIVER.replace("+", " ")
driver_encoded = urllib.parse.quote_plus(driver_normalized)

# Construir la dirección del servidor (con o sin puerto)
server_address = f"{DB_SERVER}:{DB_PORT}" if DB_PORT else DB_SERVER

# Construir la URL de conexión
if DB_TRUSTED_CONNECTION:
    # Conexión por Autenticación de Windows (Sin necesidad de usuario/contraseña)
    DATABASE_URL = f"mssql+pyodbc://{server_address}/{DB_NAME}?driver={driver_encoded}&trusted_connection=yes"
else:
    # Conexión por Autenticación de SQL Server (Con usuario y contraseña)
    DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{server_address}/{DB_NAME}?driver={driver_encoded}"

# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Crear la fábrica de sesiones con autocommit=False y autoflush=False obligatorios
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Generador de sesiones de base de datos para la inyección de dependencias de FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
