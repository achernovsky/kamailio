import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

FORWARD_TO = "test11"

@app.route('/forward-call', methods=['POST'])
def forward_call():
    logging.info("Received a request for call forwarding")

    called_number = request.form.get('called_number')
    caller_number = request.form.get('caller_number')

    logging.info(f"Caller number: {caller_number}, Called number: {called_number}")

    # Logic to determine if call forwarding is needed
    if called_number == "bob":
        logging.info(f"Call forwarding triggered for {called_number}. Forwarding to {FORWARD_TO}.")
        return jsonify({"forward_to": FORWARD_TO})
    else:
        logging.info(f"No call forwarding required for {called_number}.")
        return jsonify({"forward_to": None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
