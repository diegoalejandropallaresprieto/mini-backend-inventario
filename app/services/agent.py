# app/services/agent.py
from langgraph.graph import StateGraph, END
from typing import TypedDict
from app.infrastructure.database import ProductoRepositoryPostgres

# Estado de nuestro grafo
class AgentState(TypedDict):
    producto_consultado: str
    stock_encontrado: int | None
    mensaje_final: str

# Nodo 1: Consulta a la base de datos
def nodo_verificar_stock(state: AgentState):
    repo = ProductoRepositoryPostgres()
    stock = repo.obtener_stock(state["producto_consultado"])
    return {"stock_encontrado": stock}

# Nodo 2: Generación de respuesta (Aquí podrías integrar un LLM real)
def nodo_generar_respuesta(state: AgentState):
    stock = state["stock_encontrado"]
    producto = state["producto_consultado"]
    
    if stock is not None:
        mensaje = f"Tenemos {stock} unidades de '{producto}' en inventario."
    else:
        mensaje = f"El producto '{producto}' no existe o está agotado."
        
    return {"mensaje_final": mensaje}

# Compilación del Grafo de LangGraph
def compilar_agente_stock():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("verificar", nodo_verificar_stock)
    workflow.add_node("responder", nodo_generar_respuesta)
    
    workflow.set_entry_point("verificar")
    workflow.add_edge("verificar", "responder")
    workflow.add_edge("responder", END)
    
    return workflow.compile()