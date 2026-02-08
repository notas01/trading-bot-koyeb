FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para mejor cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear carpeta de logs
RUN mkdir -p logs

# Puerto para el servidor web
EXPOSE 8080

# Comando de inicio
CMD ["python", "main.py"]