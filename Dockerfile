# Dockerfile para IBM Code Engine
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements_api.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements_api.txt

# Copiar el código de la aplicación
COPY api_server.py .

# Exponer el puerto
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "api_server:app"]

# Made with Bob
