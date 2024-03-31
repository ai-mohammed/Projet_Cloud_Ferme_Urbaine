import numpy as np
from sklearn.ensemble import IsolationForest
from pymongo import MongoClient

# Connexion à MongoDB pour récupérer les données de capteurs
client = MongoClient('mongodb://localhost:27017/')
db = client['nom_de_la_base_de_donnees']
collection = db['sensor_data']

# Récupération des données de capteurs depuis MongoDB
documents = collection.find()
data = np.array([(float(doc['temperature'].strip('°C')), float(doc['humidity'].strip('%'))) for doc in documents if 'temperature' in doc and 'humidity' in doc])

# Vérification que des données sont récupérées
if data.size == 0:
    raise ValueError("Aucune donnée valide trouvée.")

# Étape 1: Charger les données réelles
data = np.array([
    (float(doc['temperature'].rstrip('°C')), float(doc['humidity'].rstrip('%')))
    for doc in collection.find()
])
# Étape 2: Entraînement du modèle d'Isolation Forest
# Le paramètre 'contamination' est le pourcentage estimé d'anomalies dans le jeu de données.
model = IsolationForest(n_estimators=100, contamination='auto')  # 'auto' utilise une estimation de la contamination
model.fit(data)

# Étape 3: Prédire les anomalies
predictions = model.predict(data)

# Étape 4: Identifier les anomalies
anomalies = data[predictions == -1]

print("Anomalies détectées :")
print(anomalies)

# Fermer la connexion MongoDB
client.close()

# Évaluation : Comparez les anomalies détectées avec les anomalies connues
