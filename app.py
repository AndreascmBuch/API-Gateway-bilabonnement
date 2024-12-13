from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Microservices URL'er
MICROSERVICES = {
    "kunde_api": "https://kundeapitry5-h7fnhscsdwfycqfk.northeurope-01.azurewebsites.net/",  # Kunde API
    "login_api": "https://loggeind-api-aqbehkf0exfsfjgk.northeurope-01.azurewebsites.net/"  # Login API
}

# Home directory så man kan se hvad der er i API gateway når man besøger
@app.route('/', methods=['GET'])
def home():
    """
    Gateway overview
    """
    return jsonify({
        "service": "API Gateway",
        "version": "1.0.0",
        "routes": {
            "Kunde API": "/kunde/<endpoint>",
            "Login API": "/login/<endpoint>"
        }
    })

# Kunde API proxy
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

# Login API proxy
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)