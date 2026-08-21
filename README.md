```mermaid
classDiagram
    class Producto {
        +int id
        +String nombre
        +int stock
        +int categoria_id
    }
    
    class IProductoRepository {
        <<Interface>>
        +guardar_producto(producto: Producto) Producto
        +obtener_stock(nombre_producto: String) int
    }

    class ProductoORM {
        <<SQLAlchemy Model>>
        +int id
        +String nombre
        +int stock
        +int categoria_id
    }

    class ProductoRepositoryPostgres {
        -Session db
        +guardar_producto(producto: Producto) Producto
        +obtener_stock(nombre_producto: String) int
    }

    IProductoRepository <|.. ProductoRepositoryPostgres : Implementa
    ProductoRepositoryPostgres ..> ProductoORM : Usa para mapear
    ProductoRepositoryPostgres ..> Producto : Retorna al nucleo
