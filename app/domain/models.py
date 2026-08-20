from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import List, Optional

# Entidades puras de nuestro negocio
class Categoria(BaseModel):
    id: Optional[int] = None
    nombre: str

class Producto(BaseModel):
    id: Optional[int] = None
    nombre: str
    stock: int
    categoria_id: int

# Inversión de Dependencias
class IProductoRepository(ABC):
    @abstractmethod
    def guardar_producto(self, producto: Producto) -> Producto:
        pass
    
    @abstractmethod
    def obtener_stock(self, nombre_producto: str) -> Optional[int]:
        pass