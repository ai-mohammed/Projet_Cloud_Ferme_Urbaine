from flask import Flask, request, jsonify
import base64
import msgpack
import traceback
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@data-storage-service:5432/Urban_Farm_Monitoring'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèles de données
class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(64), unique=True, nullable=False)
    sensor_version = db.Column(db.String(64), nullable=False)
    measurements = db.relationship('Measurement', backref='sensor')

class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.String(64), unique=True, nullable=False)
    plant_details = db.Column(db.Text)
    measurements = db.relationship('Measurement', backref='plant')

class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)

class Anomaly(db.Model):
    __tablename__ = 'anomalies'
    id = db.Column(db.Integer, primary_key=True)
    measurement_id = db.Column(db.Integer, db.ForeignKey('measurements.id'), nullable=False)
    anomaly_details = db.Column(db.Text)
    detected_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Assurez-vous que les tables existent
@app.before_first_request
def create_tables():
    db.create_all()

# Route pour recevoir les données
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
        
        # Extract measures
        measures = unpacked_data.get('measures', {})

        # Process temperature and humidity from measures
        temperature_celsius = measures.get('temperature', None)
        humidity_percent = measures.get('humidite', None)

        # Find or create the sensor and plant records
        sensor = Sensor.query.filter_by(sensor_id=unpacked_data['sensor_id']).first()
        if not sensor:
            sensor = Sensor(sensor_id=unpacked_data['sensor_id'], sensor_version=unpacked_data['sensor_version'])
            db.session.add(sensor)

        plant = Plant.query.filter_by(plant_id=str(unpacked_data['plant_id'])).first()
        if not plant:
            plant = Plant(plant_id=str(unpacked_data['plant_id']))
            db.session.add(plant)

        # Commit to save the sensor and plant if they are new
        db.session.commit()

        # Create a new measurement
        new_measurement = Measurement(sensor_id=sensor.id, plant_id=plant.id,
                                      temperature=temperature_celsius, humidity=humidity_percent)
        db.session.add(new_measurement)
        db.session.commit()

        # Return a success response
        return jsonify({"status": "success", "message": "Data received and saved successfully", "data": unpacked_data}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
