from flask import Flask, request, jsonify
from app.validator import validar_cedula

app = Flask(__name__)

@app.route('/validar', methods=['POST'])
def validar():
    data = request.get_json()
    cedula = data.get('cedula', '')
    resultado = validar_cedula(cedula)
    return jsonify({"cedula": cedula, "valida": resultado})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
