# Dockerfile
FROM python:3.11-slim

# 1. Establece el directorio de trabajo principal del contenedor
WORKDIR /app

# 3. Copia y instala las dependencias primero para aprovechar el caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia el resto del código de tu proyecto al contenedor
COPY . .

# 5. Expone el puerto que usará la aplicación
EXPOSE 8000

# 6. Comando para iniciar la aplicación.
#    Uvicorn ahora podrá encontrar 'app.main' porque /app está en el PYTHONPATH.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]