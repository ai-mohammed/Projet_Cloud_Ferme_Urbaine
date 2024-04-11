from flask import Flask, request, jsonify
import base64
import msgpack
import traceback
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@data-storage-service:5432/Urban_Farm_Monitoring'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Définition du modèle de données
class Measurement(db.Model):
    __tablename__ = 'measurement'
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)

    def __init__(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity

# Assurez-vous que la table existe
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/receive', methods=['POST'])
def receive_data():
    try:
        # Decode the base64 data
        base64_data = request.data
        decoded_data = base64.b64decode(base64_data)

        # Unpack the msgpack data
        unpacked_data = msgpack.unpackb(decoded_data, raw=False)

        # Log or process your data here
        print(unpacked_data)
        
        # Extraction de 'measures'
        measures = unpacked_data.get('measures', {})

        # Température
        temperature_celsius = None
        temp_keys = ['temperature', 'température']
        for key in temp_keys:
            if key in measures:
                temp_value = measures[key]
                if '°C' in temp_value:
                    temperature_celsius = float(temp_value.replace('°C', ''))
                elif '°F' in temp_value:
                    temperature_celsius = (float(temp_value.replace('°F', '')) - 32) * 5.0 / 9.0
                elif '°K' in temp_value:
                    temperature_celsius = float(temp_value.replace('°K', '')) - 273.15
                break

        # Humidité
        humidity_percent = None
        humid_keys = ['humidity', 'humidite']
        for key in humid_keys:
            if key in measures:
                humidity_value = measures[key]
                humidity_percent = float(humidity_value.replace('%', ''))
                break

        # Enregistrement dans la base de données
        new_measurement = Measurement(temperature=temperature_celsius, humidity=humidity_percent)
        db.session.add(new_measurement)
        db.session.commit()

        # Return a success response
        return jsonify({"status": "success", "message": "Data received and saved successfully", "data": unpacked_data}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
