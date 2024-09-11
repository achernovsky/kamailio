from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/forward-call', methods=['POST'])
def forward_call():
    called_number = request.form.get('called_number')
    caller_number = request.form.get('caller_number')

    # Logic to determine if call forwarding is needed
    if called_number == "123":
        return jsonify({"forward_to": "test11"})
    else:
        return jsonify({"forward_to": None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)