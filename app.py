from flask import Flask, jsonify, request
import requests
from swagger.config import init_swagger
from flasgger import swag_from

app = Flask(__name__)
swagger = init_swagger(app)

# Microservices URL'er
MICROSERVICES = {
    "kunde_api": "https://kundeapitry5-h7fnhscsdwfycqfk.northeurope-01.azurewebsites.net/",  # Kunde API
    "login_api": "https://loggeind-api-aqbehkf0exfsfjgk.northeurope-01.azurewebsites.net/",  # Login API
    "bildatabase_api": "https://bildatabasedemo-hzfbegh6eqfraqdd.northeurope-01.azurewebsites.net/", # Bildatabase API
    "abonnement_api":"https://abonnement-beczhgfth9axdzd9.northeurope-01.azurewebsites.net/", # Abonnement API
    "damage_api":"https://skade-demo-b2awcyb4gedxdnhj.northeurope-01.azurewebsites.net/", # Skadeservice API 
    "calculate_api": "https://skadeberegner-d9fferbzcgddfycm.northeurope-01.azurewebsites.net/", # Beregning service API 
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
            "Login API": "/login/<endpoint>",
            "Cars API": "/cars/<endpoint>",
            "Abonnement API": "/abonnement/<endpoint>",
            "Damage API": "/damage/<endpoint>",
            "Calculate API":"/"
        }
    })

# Kunde API proxy
@app.route('/kunde/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@swag_from('swagger/kunde.yaml')
def proxy_kunde(path):
    """
    Proxy requests to Kunde API
    """
     # Kun inkluder json for POST og PUT anmodninger
    if request.method in ['POST', 'PUT']:
        data = request.get_json()
    else:
        data = None
        
    service_url = f"{MICROSERVICES['kunde_api']}/{path}"
    response = requests.request(
        method=request.method,  # Use the same HTTP method
        url=service_url,        # Forward to the target microservice
        headers={key: value for key, value in request.headers if key != 'Host'},  # Forward headers
        json=data
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

# Bil API
@app.route('/cars/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@swag_from('swagger/cars.yaml')
def proxy_cars(path):
    service_url = f"{MICROSERVICES['bildatabase_api']}/{path}"
    response = requests.request(
        method=request.method,
        url=service_url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        json=request.get_json() if request.method in ['POST', 'PUT'] else None
    )
    return jsonify(response.json()), response.status_code

 # Abonnement API
@app.route('/abonnement/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@swag_from('swagger/abonnement.yaml')
def proxy_abonnement(path):
    """
    Proxy requests to Abonnement API
    """
    service_url = f"{MICROSERVICES['abonnement_api']}/{path}"
    response = requests.request(
        method=request.method,  
        url=service_url,        
        headers={key: value for key, value in request.headers if key != 'Host'},  
        json=request.get_json()  
    )
    return jsonify(response.json()), response.status_code

# Damage API
@app.route('/damage/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@swag_from('swagger/damage.yaml')   
def proxy_damage(path):
    """
    Proxy requests to Damage API
    """
    service_url = f"{MICROSERVICES['damage_api']}/{path}"

    # For POST and PUT, include JSON body
    if request.method in ['POST', 'PUT']:
        data = request.get_json()
    else:
        data = None

    # Send the proxied request
    response = requests.request(
        method=request.method,  
        url=service_url,        
        headers={key: value for key, value in request.headers if key != 'Host'},  
        json=data  # Only send JSON for POST and PUT
    )
    
    return jsonify(response.json()), response.status_code

# Calculate API
@app.route('/calculate/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@swag_from('swagger/calculate.yaml')
def proxy_calculate(path):
    """
    Proxy requests to Calculate API
    """
    service_url = f"{MICROSERVICES['calculate_api']}/{path}"
    response = requests.request(
        method=request.method,  
        url=service_url,        
        headers={key: value for key, value in request.headers if key != 'Host'},  
        json=request.get_json()  
    )
    return jsonify(response.json()), response.status_code


if __name__ == '__main__':
    app.run()