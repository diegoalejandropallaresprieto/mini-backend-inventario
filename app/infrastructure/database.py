import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from app.domain.models import Producto, IProductoRepository

# 1. Leer la URL desde el archivo .env o desde la nube
# Render inyectará su propia URL aquí. Si estás en tu PC y no la inyecta, usará tu cadena local como plan B.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://inventario_db_prod_user:HlcblWrtUaT8RKPwHLJDr1dKY44m0xPC@dpg-da3oq78u01pc73c3qeug-a/inventario_db_prod")

# 2. Validación de seguridad para SQLAlchemy en Render
# Render a veces entrega URLs que empiezan con 'postgres://'. SQLAlchemy exige 'postgresql://'
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos ORM 
class ProductoORM(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    stock = Column(Integer)
    categoria_id = Column(Integer)

Base.metadata.create_all(bind=engine)

class ProductoRepositoryPostgres(IProductoRepository):
    def __init__(self):
        self.db = SessionLocal()

    def guardar_producto(self, producto: Producto) -> Producto:
        db_producto = ProductoORM(nombre=producto.nombre, stock=producto.stock, categoria_id=producto.categoria_id)
        
        try:
            self.db.add(db_producto)
            self.db.commit()
            self.db.refresh(db_producto)
            producto.id = db_producto.id
            return producto
        except Exception as e:
            self.db.rollback()  # ¡Esta es la magia! Si falla, "limpia" la sesión para que no se trabe.
            raise e

    def obtener_stock(self, nombre_producto: str) -> int | None:
        db_producto = self.db.query(ProductoORM).filter(ProductoORM.nombre == nombre_producto).first()
        if db_producto:
            return db_producto.stock
        return None