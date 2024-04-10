from flask import Flask, request, jsonify
import base64
import msgpack
import traceback

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

        # Return a success response
        return jsonify({"status": "success", "message": "Data received successfully", "data": unpacked_data}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)