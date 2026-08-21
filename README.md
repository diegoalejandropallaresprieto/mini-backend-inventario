```
classDiagram
    namespace Capa_Dominio {
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
    }

    namespace Capa_Infraestructura {
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
    }

    %% Relaciones (SOLID: Inversión de Dependencias)
    IProductoRepository <|.. ProductoRepositoryPostgres : Implementa
    ProductoRepositoryPostgres ..> ProductoORM : Usa para mapear a BD
    ProductoRepositoryPostgres ..> Producto : Retorna al núcleo
```