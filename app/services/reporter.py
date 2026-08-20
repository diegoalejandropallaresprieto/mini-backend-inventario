import os
import httpx
from openai import OpenAI
from dotenv import load_dotenv
from app.infrastructure.database import SessionLocal, ProductoORM

# Cargar las credenciales ocultas
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configurar el cliente para que apunte a Groq en lugar de OpenAI
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def generar_y_enviar_reporte():
    db = SessionLocal()
    try:
        productos = db.query(ProductoORM).all()
        datos_inventario = "\n".join([f"- {p.nombre}: {p.stock} unidades" for p in productos])
        
        if not datos_inventario:
            datos_inventario = "El inventario está vacío."

        # Petición a la IA (usando Llama 3)
        respuesta_ia = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Eres un analista de datos logísticos. Resume este inventario en un mensaje corto y profesional para Telegram, destacando si hay bajo stock (menos de 10 unidades)."},
                {"role": "user", "content": datos_inventario}
            ]
        )
        mensaje_final = respuesta_ia.choices[0].message.content

        # Envío por Telegram
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        httpx.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje_final})
        print("✅ Reporte diario enviado a Telegram con éxito.")
        
    finally:
        db.close()