# Usar imagen base de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para caching de capas)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos
COPY . .

# Crear directorio para logs
RUN mkdir -p logs

# Exponer puerto (Koyeb usa 8000 por defecto, pero mantenemos 8080)
EXPOSE 8080

# Variable de entorno para Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
