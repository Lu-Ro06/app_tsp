from flask import Flask, render_template, request, jsonify
import math
import random

app = Flask(__name__)

def distancia(coor1, coor2):
    lat1, lon1 = coor1
    lat2, lon2 = coor2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i+1]])
    return total

def simulated_annealing(ruta, coord, T, tasa_enfriamiento):
    T_MIN = 0
    V_enfriamiento = 100

    while T > T_MIN:
        dist_actual = evalua_ruta(ruta, coord)

        for _ in range(V_enfriamiento):
            i, j = random.sample(range(len(ruta)), 2)
            ruta_tmp = ruta[:]
            ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]

            dist_nueva = evalua_ruta(ruta_tmp, coord)
            delta = dist_actual - dist_nueva

            if delta > 0 or random.random() < math.exp(-delta / T):
                ruta = ruta_tmp[:]
                break

        T -= tasa_enfriamiento

    return ruta

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    ciudades = data['ciudades']
    temperatura = data['temperatura']
    tasa_enfriamiento = data['tasa_enfriamiento']

    coord = {ciudad['nombre']: (ciudad['latitud'], ciudad['longitud']) for ciudad in ciudades}
    ruta = list(coord.keys())
    random.shuffle(ruta)

    ruta_optima = simulated_annealing(ruta, coord, temperatura, tasa_enfriamiento)
    distancia_total = evalua_ruta(ruta_optima, coord)

    return jsonify({'ruta': ruta_optima, 'distancia': distancia_total})

if __name__ == "__main__":
    app.run(debug=True)
