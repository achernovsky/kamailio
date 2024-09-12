from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy users database for demonstration purposes
users_db = {
    "test11": "nothing8",
    "bob": "bob1234"
}

@app.route('/auth', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in users_db and users_db[username] == password:
        return jsonify({"authenticated": True})
    else:
        return jsonify({"authenticated": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
