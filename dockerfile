# --- Etapa 1: BASE ---

# Instala las dependencias (común entre dev y prod)
FROM python:3.11-slim as BASE

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Etapa 2: PRODUCCIÓN ---

# Esta etapa crea la imagen final y optimizada para producción.
FROM BASE AS PROD

# Copia solo el código necesario de la aplicación
COPY ./app /app/app
COPY ./main.py /app/main.py

# Comando para iniciar la aplicación en modo producción (sin --reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Etapa 3: DESARROLLO ---

# Esta etapa se usa solo para el entorno de desarrollo local.
FROM BASE AS DEV

# Expone el puerto
EXPOSE 8000

# Comando para iniciar la aplicación con recarga automática
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]