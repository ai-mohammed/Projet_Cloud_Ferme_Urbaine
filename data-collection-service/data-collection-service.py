from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import base64
import msgpack
import traceback
from datetime import datetime
import re

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@data-storage-service:5432/Urban_Farm_Monitoring'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle pour les capteurs
class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(64), unique=True, nullable=False)
    sensor_version = db.Column(db.String(64), nullable=False)
    measurements = db.relationship('Measurement', backref='sensor')

# Modèle pour les plantes
class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.String(64), unique=True, nullable=False)
    plant_details = db.Column(db.Text)
    measurements = db.relationship('Measurement', backref='plant')

# Modèle pour les mesures
class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)

# Assurez-vous que les tables existent avec la bonne structure au démarrage
@app.before_first_request
def create_or_update_tables():
    # Mettre à jour ou créer les tables
    db.reflect()
    db.drop_all()
    db.create_all()

def clean_and_convert_data(measures):
    """Nettoie et convertit les mesures de température et d'humidité."""
    temperature_celsius = None
    humidity_percent = None
    
    # Traitement de la température
    temp_keys = ['temperature', 'température']  # Support des clés en anglais et en français
    for key in temp_keys:
        if key in measures:
            temp_value = measures[key]
            # Retirer les caractères non-numériques, sauf les indicateurs d'unité
            temp_value = re.sub(r"[^\d.°CFK]", "", temp_value)
            
            if '°C' in temp_value:
                temperature_celsius = float(temp_value.replace('°C', ''))
            elif '°F' in temp_value:
                temperature_fahrenheit = float(temp_value.replace('°F', ''))
                temperature_celsius = (temperature_fahrenheit - 32) * 5.0 / 9.0
            elif '°K' in temp_value:
                temperature_kelvin = float(temp_value.replace('°K', ''))
                temperature_celsius = temperature_kelvin - 273.15
            break  # Arrêter après avoir trouvé la première clé valide
    
    # Traitement de l'humidité
    humid_keys = ['humidity', 'humidite']  # Support des clés en anglais et en français
    for key in humid_keys:
        if key in measures:
            humidity_value = measures[key]
            # Retirer les caractères non-numériques, sauf le symbole pourcent
            humidity_value = re.sub(r"[^\d.%]", "", humidity_value)
            if '%' in humidity_value:
                humidity_percent = float(humidity_value.replace('%', ''))
            break  # Arrêter après avoir trouvé la première clé valide
    
    # Vérifier que les deux mesures essentielles ont été trouvées et nettoyées
    if temperature_celsius is None or humidity_percent is None:
        raise ValueError("Temperature or humidity data is missing or invalid.")
    
    return {
        'temperature': temperature_celsius,
        'humidity': humidity_percent
    }

# Utiliser cette fonction dans la route de réception des données
@app.route('/receive', methods=['POST'])
def receive_data():
    try:
        # Decode the base64 data
        base64_data = request.data
        decoded_data = base64.b64decode(base64_data)

        # Unpack the msgpack data
        unpacked_data = msgpack.unpackb(decoded_data, raw=False)

        # Nettoyer et convertir les mesures
        measures = unpacked_data.get('measures', {})
        clean_data = clean_and_convert_data(measures)

        # Trouver ou créer le capteur
        sensor = Sensor.query.filter_by(sensor_id=unpacked_data['sensor_id']).first()
        if not sensor:
            sensor = Sensor(sensor_id=unpacked_data['sensor_id'], sensor_version=unpacked_data['sensor_version'])
            db.session.add(sensor)

        # Trouver ou créer la plante
        plant = Plant.query.filter_by(plant_id=str(unpacked_data['plant_id'])).first()
        if not plant:
            plant = Plant(plant_id=str(unpacked_data['plant_id']), plant_details='Details about the plant')
            db.session.add(plant)

        db.session.commit()  # Assurer que le capteur et la plante sont sauvegardés pour obtenir leurs ID

        # Créer une nouvelle mesure
        new_measurement = Measurement(
            sensor_id=sensor.id,
            plant_id=plant.id,
            temperature=clean_data['temperature'],
            humidity=clean_data['humidity'],
            time=datetime.utcnow()
        )
        db.session.add(new_measurement)
        db.session.commit()

        return jsonify({"status": "success", "message": "Data received and saved successfully", "data": unpacked_data}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)