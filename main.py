from fastapi import FastAPI, HTTPException
from app.domain.models import Producto
from app.infrastructure.database import ProductoRepositoryPostgres
from app.services.agent import compilar_agente_stock
from fastapi.responses import RedirectResponse

app = FastAPI(title="Mini Backend de Inventario")

@app.get("/")
def read_root():
    # Redirige automáticamente a los usuarios a la pantalla de /docs
    return RedirectResponse(url="/docs")

repo = ProductoRepositoryPostgres()
agente = compilar_agente_stock()

@app.post("/productos/")
def crear_producto(producto: Producto):
    try:
        nuevo_producto = repo.guardar_producto(producto)
        return {"mensaje": "Producto guardado", "producto": nuevo_producto}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/consultar-agente/{nombre_producto}")
def consultar_stock_con_agente(nombre_producto: str):
    # se ejecuta el flujo de LangGraph
    estado_inicial = {"producto_consultado": nombre_producto}
    resultado = agente.invoke(estado_inicial)
    
    return {"agente_dice": resultado["mensaje_final"]}