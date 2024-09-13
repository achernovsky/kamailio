from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# Dummy users database for demonstration purposes
users_db = {
    "test11": "nothing8",
    "bob": "bob1234"
}

def calculate_response(username, realm, password, nonce, method, uri):
    # Calculate HA1
    ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode()).hexdigest()
    
    # Calculate HA2
    ha2 = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()
    
    # Calculate the response
    response = hashlib.md5(f"{ha1}:{nonce}:{ha2}".encode()).hexdigest()
    
    return response

@app.route('/auth', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    realm = request.form.get('realm')
    nonce = request.form.get('nonce')
    uri = request.form.get('uri')
    response = request.form.get('response')
    method = request.form.get('method')

    if username not in users_db:
        return jsonify({"authenticated": False, "reason": "User not found"})

    password = users_db[username]

    expected_response = calculate_response(username, realm, password, nonce, method, uri)

    if response == expected_response:
        return jsonify({"authenticated": True})
    else:
        return jsonify({"authenticated": False, "reason": "Invalid credentials"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
