from sqlalchemy.orm import Session
from domain.entities.compania import Compania
from domain.entities.empleado import Empleado

def seed_data(db: Session):
    """Inserta datos de prueba si la base de datos está vacía."""
    # Verificar si ya existen compañías en la base de datos
    if db.query(Compania).first() is not None:
        return  # Ya existen datos, no se requiere sembrado

    # Definir compañías
    c1 = Compania(nombre="Tech Solutions S.A.S", direccion="Calle 45 # 10-20", telefono="3001234567")
    c2 = Compania(nombre="Innovatech Colombia", direccion="Av. El Dorado # 68-50", telefono="6017654321")
    c3 = Compania(nombre="DataCorp Ltda", direccion="Carrera 7 # 32-16", telefono="3157894561")

    db.add_all([c1, c2, c3])
    db.flush()  # Para obtener los IDs autogenerados de las compañías

    # Definir 10 empleados distribuidos: 3 en c1, 3 en c2, 4 en c3
    empleados = [
        # Compañía 1 (Tech Solutions S.A.S)
        Empleado(
            nombre="Juan",
            apellido="Perez",
            correo="juan.perez@techsolutions.com",
            cargo="Desarrollador",
            salario=3500000.0,
            compania_id=c1.id
        ),
        Empleado(
            nombre="Maria",
            apellido="Gomez",
            correo="maria.gomez@techsolutions.com",
            cargo="Analista",
            salario=4000000.0,
            compania_id=c1.id
        ),
        Empleado(
            nombre="Carlos",
            apellido="Rodriguez",
            correo="carlos.rod@techsolutions.com",
            cargo="Scrum Master",
            salario=6000000.0,
            compania_id=c1.id
        ),
        
        # Compañía 2 (Innovatech Colombia)
        Empleado(
            nombre="Ana",
            apellido="Martinez",
            correo="ana.martinez@innovatech.co",
            cargo="Tester",
            salario=2500000.0,
            compania_id=c2.id
        ),
        Empleado(
            nombre="Luis",
            apellido="Sanchez",
            correo="luis.sanchez@innovatech.co",
            cargo="Desarrollador",
            salario=4500000.0,
            compania_id=c2.id
        ),
        Empleado(
            nombre="Laura",
            apellido="Diaz",
            correo="laura.diaz@innovatech.co",
            cargo="DevOps",
            salario=5500000.0,
            compania_id=c2.id
        ),
        
        # Compañía 3 (DataCorp Ltda)
        Empleado(
            nombre="Diego",
            apellido="Giraldo",
            correo="diego.giraldo@datacorp.com",
            cargo="Analista",
            salario=3800000.0,
            compania_id=c3.id
        ),
        Empleado(
            nombre="Sofia",
            apellido="Torres",
            correo="sofia.torres@datacorp.com",
            cargo="Desarrollador",
            salario=4800000.0,
            compania_id=c3.id
        ),
        Empleado(
            nombre="Andres",
            apellido="Castro",
            correo="andres.castro@datacorp.com",
            cargo="DevOps",
            salario=5800000.0,
            compania_id=c3.id
        ),
        Empleado(
            nombre="Valentina",
            apellido="Ruiz",
            correo="valentina.ruiz@datacorp.com",
            cargo="Tester",
            salario=2800000.0,
            compania_id=c3.id
        )
    ]

    db.add_all(empleados)
    db.commit()
