import requests

from flask import (
    Flask,
    render_template,
    request,
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/base1_python'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import City

ciudades = {
    "Buenos Aires": {"lat": -34.6037, "lon": -58.3816},
    "Córdoba": {"lat": -31.4201, "lon": -64.1888},
    "Madrid": {"lat": 40.4168, "lon": -3.7038},
    "Nueva York": {"lat": 40.7128, "lon": -74.0060},
    "Tokio": {"lat": 35.6895, "lon": 139.6917},
    "París": {"lat": 48.8566, "lon": 2.3522},
    "Londres": {"lat": 51.5074, "lon": -0.1278},
    "Sídney": {"lat": -33.8688, "lon": 151.2093},
    "Ciudad de México": {"lat": 19.4326, "lon": -99.1332},
    "El Cairo": {"lat": 30.0444, "lon": 31.2357}
}

@app.route("/")
def index():
    return render_template("index.html", ciudades=ciudades)

@app.route("/clima")
def ciudad():
    # /users?cantidad=2&pagina=10
    print(request.method)

    elegido = request.args.get('ciudad', str)
    lati = ciudades[elegido]["lat"]
    long = ciudades[elegido]["lon"]
    
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lati}&longitude={long}&current_weather=true")
    data = response.json()
    ciudad = data['current_weather']

    return render_template(
        "clima.html",
        listado_ciudades = ciudades,
        datos = ciudad,
        ciudad_elegida = elegido
    )


""" 
@app.route("/clima")
def ciudad(nombre):
    # /users?cantidad=2&pagina=10
    
    ciudad_data = ciudades.get(nombre)
    if ciudad_data:
        return render_template("clima.html", nombre=nombre, datos=ciudad_data)
    else:
        return "Ciudad no encontrada", 404
 """

"""

@app.route("/clima")
def usuarios():
    # /users?cantidad=2&pagina=10
    print(request.method)
    cant = request.args.get('cantidad','5', int)
    response = requests.get(f"https://randomuser.me/api/?results={cant}")
    data = response.json()
    user_list = data['results']
    return render_template(
        "clima.html",
        listado_usuarios = user_list
    )
"""