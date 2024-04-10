# Utilise l'image officielle Python comme image parente
FROM python:3.8

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances dans le conteneur
COPY requirements.txt .

# Installe Streamlit et d'autres dépendances spécifiées dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste des fichiers de l'application dans le conteneur
COPY . .

# Expose le port sur lequel Streamlit s'exécute
EXPOSE 8501

# Commande pour exécuter l'application Streamlit
CMD ["streamlit", "run", "app.py"]
