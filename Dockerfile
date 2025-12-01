FROM python:3.9-alpine

WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar toda la aplicación
COPY . .

EXPOSE 5000

CMD ["python", "app/api.py"]