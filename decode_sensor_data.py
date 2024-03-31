from flask import Flask, request, jsonify
import base64
import msgpack
from pymongo import MongoClient

app = Flask(__name__)

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['nom_de_la_base_de_donnees']
collection = db['sensor_data']

@app.route('/sensor', methods=['POST'])
def process_sensor_data():
    # Récupérer les données de capteurs encodées en Base64 dans le corps de la requête POST
    data_base64 = request.data

    # Décodage et désérialisation
    data_msgpack = base64.b64decode(data_base64)
    data = msgpack.unpackb(data_msgpack, raw=False)

    # Extraction des données
    sensor_id = data.get("sensor_id")
    sensor_version = data.get("sensor_version")
    plant_id = data.get("plant_id")
    timestamp = data.get("time")
    measures = data.get("measures", {})
    temperature = measures.get("temperature")
    humidity = measures.get("humidity")

    # Document à insérer
    document = {
        "sensor_id": sensor_id,
        "sensor_version": sensor_version,
        "plant_id": plant_id,
        "time": timestamp,
        "temperature": temperature,
        "humidity": humidity
    }

    # Insertion du document dans MongoDB
    try:
        collection.insert_one(document)
        return jsonify({"message": "Document inséré avec succès."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Fermeture de la connexion MongoDB à l'arrêt de l'application
@app.teardown_appcontext
def close_db(error):
    if client:
        client.close()

if __name__ == '__main__':
    app.run(debug=True)
