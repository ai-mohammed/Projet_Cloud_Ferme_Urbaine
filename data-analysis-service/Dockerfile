# Utilise une image Python officielle comme image parente
FROM python:3.8-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances dans le conteneur
COPY requirements.txt .

# Installe les packages Python spécifiés dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie le contenu du répertoire data-analysis-service local dans le conteneur
COPY . .

# Commande pour exécuter le script analyze.py
CMD ["python", "./analyze.py"]
