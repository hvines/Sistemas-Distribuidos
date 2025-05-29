# Imagen base
FROM python:3.11

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos al contenedor
COPY requirements.txt .
COPY app.py .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto
CMD ["python", "app.py"]