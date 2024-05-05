FROM python:3.8-slim

# Copier le fichier requirements.txt dans l'image
COPY requirements.txt /app/requirements.txt

WORKDIR /app

# Mise à jour de pip
RUN pip install --no-cache-dir --upgrade pip

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code dans l'image
COPY main.py /app/main.py

# Commande pour lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
