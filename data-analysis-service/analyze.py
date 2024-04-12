from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@data-storage-service:5432/Urban_Farm_Monitoring'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, nullable=False)
    plant_id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)

@app.route('/data', methods=['GET'])
def get_data():
    measurements = Measurement.query.all()
    data = [{'id': m.id, 'temperature': m.temperature, 'humidity': m.humidity} for m in measurements]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
