from flask import Flask, jsonify, request
from app.validator import validar_con_tiempo, verificar_en_servicio_externo
import logging

# Configurar logging para auditoría
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validate_endpoint():
    """Endpoint para validar datos enviados en formato JSON."""
    try:
        data = request.get_json(force=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Formato inválido, debe ser un objeto JSON"}), 400

        result = validar_con_tiempo(data)

        if result.get("valido"):
            externo = verificar_en_servicio_externo(data.get("email"))
            result.update(externo)

        logging.info("Validación completada correctamente.")
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Error interno: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Verifica si el servicio está activo."""
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
