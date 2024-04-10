from flask import Flask, request, jsonify
import base64
import msgpack
import traceback
import psycopg
import os

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

        # Env variables
        host=os.getenv("postgtres-server")
        port=os.getenv("5432")
        database=os.getenv("POSTGRES_DB")
        user=os.getenv("POSTGRES_USER")
        password=os.getenv("POSTGRES_PASSWORD")

        # Connect to PostgreSQL server
        conn = psycopg.connect(f"dbname='{database}' user='{user}' host='{host}' port='{port}' password='{password}'")
        cur = conn.cursor()
        
        # Function to insert data into a table
        def insert_into_table(conn, cur, table, data):
            # Create a cursor from the connection

            # Create the SQL command
            columns = ', '.join(data.keys())
            values = ', '.join(f'%({key})s' for key in data.keys())
            sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"

            # Execute the SQL command
            cur.execute(sql, data)

            # Commit the changes
            conn.commit()

        
        sensor={
            'ID': sensor_id,
            'Provider': sensor_version
        }
        plant={
            'ID': plant_id
        }
        
        if cur.execute("SELECT ID FROM Measurements") == []:
            measurement_id = 0
        else:
            measurement_id = cur.execute("SELECT MAX(ID) FROM Measurements") + 1
        measurement={
            'ID': measurement_id,
            'Sensor_ID': sensor_id,
            'Plant_ID': plant_id,
            'Temperature': temperature_celsius,
            'Humidity': humidity_percent,
            'Timestamp': time
        }
        
        insert_into_table(conn, cur, 'Sensors', sensor)
        insert_into_table(conn, cur, 'Plants', plant)
        insert_into_table(conn, cur, 'Measurments', measurement)
        
        cur.close()

        # Return a success response
        return jsonify({"status": "success", "message": "Data received successfully", "data": unpacked_data}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 400
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)