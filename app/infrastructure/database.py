from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from app.domain.models import Producto, IProductoRepository

DATABASE_URL = "postgresql://postgres:dcadml25@localhost:5432/inventario_db"
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