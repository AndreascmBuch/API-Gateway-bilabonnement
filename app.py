from flask import Flask, jsonify, request
import requests
from swagger.config import init_swagger
from flasgger import swag_from

app = Flask(__name__)
swagger = init_swagger(app)

# Microservices URL'er
MICROSERVICES = {
    "kunde_api": "https://kundeapitry5-h7fnhscsdwfycqfk.northeurope-01.azurewebsites.net/",  # Kunde API
    "login_api": "https://loggeind-api-aqbehkf0exfsfjgk.northeurope-01.azurewebsites.net/"  # Login API
}

# Home directory så man kan se hvad der er i API gateway når man besøger
@app.route('/', methods=['GET'])
@swag_from('swagger/home.yaml')
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
@swag_from('swagger/proxy_kunde.yaml')
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

# Login API - Register
@app.route('/login/register', methods=['POST'])
@swag_from('swagger/register.yaml')
def proxy_register():
    """
    Proxy requests to Login API - Register
    """
    service_url = f"{MICROSERVICES['login_api']}/register"
    response = requests.post(
        url=service_url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        json=request.get_json()
    )
    return jsonify(response.json()), response.status_code

# Login API - Login
@app.route('/login/login', methods=['POST'])
@swag_from('swagger/login.yaml')
def proxy_login():
    """
    Proxy requests to Login API - Login
    """
    service_url = f"{MICROSERVICES['login_api']}/login"
    response = requests.post(
        url=service_url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        json=request.get_json()
    )
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(port=5000, debug=True)