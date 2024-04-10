from flask import Flask, request, jsonify
import base64
import msgpack
import traceback
from data_storage_service.models import conn, cur




app = Flask(__name__)

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
        
        # Extraction des données
        sensor_id = unpacked_data.get('sensor_id')
        sensor_version = unpacked_data.get('sensor_version')
        plant_id = unpacked_data.get('plant_id')
        time = unpacked_data.get('time')
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
                humidity_percent = float(measures[key])
                break

# Insérer les données dans la table Sensors
        cur.execute('''
    INSERT INTO Sensors (ID, Provider, Location) 
    VALUES (%s, %s, %s)
''', (sensor_id, sensor_version, 'Location'))

# Insérer les données dans la table Plants
        cur.execute('''
    INSERT INTO Plants (ID, Species, Optimal_Temp, Optimal_Humidity) 
    VALUES (%s, %s, %s, %s)
''', (plant_id, 'Species', [20.0, 30.0], [40.0, 60.0]))

# Insérer les données dans la table Measurements
        cur.execute('''
    INSERT INTO Measurements (Sensor_ID, Plant_ID, Temperature, Humidity, Timestamp) 
    VALUES (%s, %s, %s, %s, %s)
''', (sensor_id, plant_id, temperature_celsius, humidity_percent, time))


        # Commit les changements
        conn.commit()

        # Return a success response
        return jsonify({"status": "success", "message": "Data received successfully", "data": unpacked_data}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 400
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)