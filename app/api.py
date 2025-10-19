from flask import Flask, jsonify, request
from app.validator import validar_con_tiempo, verificar_en_servicio_externo

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "running"}), 200

@app.route('/validar', methods=['POST'])
def validar():
    data = request.get_json()
    cedula = data.get("cedula", "")
    resultado = validar_con_tiempo(cedula)

    # Agregamos verificación externa si la cédula es válida
    if resultado.get("valida"):
        externo = verificar_en_servicio_externo(cedula)
        resultado.update(externo)

    return jsonify(resultado), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
