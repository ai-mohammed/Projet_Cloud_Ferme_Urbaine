# Utilisez une image de base avec Python et pip installés
FROM python:3.8

# Réglez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le fichier des dépendances dans le répertoire de travail
COPY requirements.txt .

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le contenu du répertoire local src dans le répertoire de travail
COPY . .

# Exposez le port sur lequel Streamlit s'exécute
EXPOSE 8501

# Lancez Streamlit
CMD ["streamlit", "run", "alert_receiver.py", "--server.address=0.0.0.0", "--server.port=8501"]
