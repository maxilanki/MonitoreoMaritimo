# Usar una imagen oficial de Python ligera
FROM python:3.11-slim

# Evitar que Python genere archivos .pyc o mantenga el buffer de log
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Definir directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto a la imagen
COPY . .

# Exponer el puerto del contenedor
EXPOSE 5000

# Comando para ejecutar la aplicación con Gunicorn + Eventlet
CMD ["gunicorn", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "--bind", "0.0.0.0:5000", "app:app"]