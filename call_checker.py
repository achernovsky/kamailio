from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Define the IPs you want to block
BLOCKED_SOURCE_IP = "84.25.58.187"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.FileHandler("call_logs.log"), logging.StreamHandler()])

@app.route('/check-call', methods=['POST'])
def check_call():
    logging.info(f"Received request: {request.form}")
    data = request.form
    source_ip = data.get('source_ip')
    destination_ip = data.get('destination_ip')
    user_alias = request.form.get('user_alias')  # Get the custom X-UserAlias

    print(f"User Alias: {user_alias}")

    # Check if the source IP matches the blocked IP
    if source_ip == BLOCKED_SOURCE_IP:
        logging.info(f"Blocked call from {source_ip} to {destination_ip}")
        return jsonify({"allow": False}), 200  # Block the call
    else:
        logging.info(f"Allowed call from {source_ip} to {destination_ip}")
        return jsonify({"allow": True}), 200   # Allow the call

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
