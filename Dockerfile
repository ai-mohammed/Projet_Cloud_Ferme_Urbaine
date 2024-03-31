# Dockerfile pour l'API de Réception des Données
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install Flask requests
CMD ["python", "data_ingestion_api.py"]

# Dockerfile pour le Serveur d'Application
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install Flask SQLAlchemy
CMD ["python", "application_server.py"]

# Dockerfile pour l'Interface Utilisateur
FROM node:14
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]

