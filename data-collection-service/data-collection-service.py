from flask import Flask, request, jsonify
import base64
import msgpack

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

        # Return a success response
        return jsonify({"status": "success", "message": "Data received successfully", "data": unpacked_data}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
