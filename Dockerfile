# Usa una imagen oficial y ligera de Python
FROM python:3.13-slim

# Crea y muévete a la carpeta /app dentro del contenedor
WORKDIR /app

# Copia primero los requerimientos y descárgalos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu código
COPY . .

# Expone el puerto que usará FastAPI
EXPOSE 8000

# Comando final para arrancar el servidor web
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]