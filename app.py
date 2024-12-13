from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Microservices URL'er
MICROSERVICES = {
    "kunde_api": "http://127.0.0.1:5000",  # Kunde API
    "login_api": "http://127.0.0.1:5002"  # Login API
}

@app.route('/kunde/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_kunde(path):
    """
    Proxy requests to Kunde API
    """
    service_url = f"{MICROSERVICES['kunde_api']}/{path}"
    response = requests.request(
        method=request.method,  # Use the same HTTP method
        url=service_url,        # Forward to the target microservice
        headers={key: value for key, value in request.headers if key != 'Host'},  # Forward headers
        json=request.get_json()  # Forward JSON payload (if any)
    )
    return jsonify(response.json()), response.status_code

@app.route('/login/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_login(path):
    """
    Proxy requests to Login API
    """
    service_url = f"{MICROSERVICES['login_api']}/{path}"
    response = requests.request(
        method=request.method,
        url=service_url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        json=request.get_json()
    )
    return jsonify(response.json()), response.status_code