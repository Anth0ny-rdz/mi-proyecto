from flask import Flask, request, jsonify
from app.validator import (
    validar_cedula,
    validar_datos,
    validar_con_tiempo,
    verificar_en_servicio_externo
)
import os
import ldclient
from ldclient.config import Config

app = Flask(__name__)

# ========== LAUNCHDARKLY INTEGRATION ==========
# Inicializar LaunchDarkly
sdk_key = os.environ.get('LAUNCHDARKLY_SDK_KEY', '')
if sdk_key:
    ldclient.set_config(Config(sdk_key))
    client = ldclient.get()
    print("✅ LaunchDarkly inicializado correctamente")
else:
    client = None
    print("⚠️  LaunchDarkly no configurado - usando valores por defecto")

def get_feature_flag(user_key, feature_flag_key, default=False):
    """
    Obtiene el estado de un feature flag desde LaunchDarkly
    """
    if client:
        user = {
            "key": user_key,
            "custom": {
                "groups": "users"
            }
        }
        return client.variation(feature_flag_key, user, default)
    return default
# ========== FIN LAUNCHDARKLY ==========

@app.route("/")
def home():
    """Ruta de prueba para verificar si la API está viva."""
    # Usar feature flag para nuevo mensaje
    user_ip = request.remote_addr or "anonymous"
    if get_feature_flag(user_ip, 'nuevo-mensaje-bienvenida', False):
        return jsonify({"mensaje": "🚀 API de validación activa - Nueva Versión!"}), 200
    else:
        return jsonify({"mensaje": "API de validación activa"}), 200

@app.route("/status")
def status():
    """Devuelve el estado de la API (para pruebas de Jenkins)."""
    # Feature flag para mostrar información adicional
    user_ip = request.remote_addr or "anonymous"
    if get_feature_flag(user_ip, 'status-detallado', False):
        return jsonify({
            "status": "ok", 
            "message": "API funcionando correctamente",
            "version": "2.0.0",
            "features": {
                "nuevo-mensaje-bienvenida": get_feature_flag(user_ip, 'nuevo-mensaje-bienvenida', False),
                "status-detallado": True
            }
        }), 200
    else:
        return jsonify({"status": "ok", "message": "API funcionando correctamente"}), 200

@app.route("/validar", methods=["POST"])
def validar_cedula_endpoint():
    """
    Endpoint que valida una cédula ecuatoriana.
    """
    # Feature flag para validación mejorada
    user_ip = request.remote_addr or "anonymous"
    validacion_mejorada = get_feature_flag(user_ip, 'validacion-mejorada', False)
    
    data = request.get_json()
    if not data or "cedula" not in data:
        return jsonify({"error": "Debe incluir el campo 'cedula'"}), 400

    resultado = validar_cedula(data["cedula"])
    
    # Añadir información del feature flag si está activo
    if validacion_mejorada:
        resultado["feature_flags"] = {
            "validacion_mejorada": True,
            "version": "2.0"
        }
    
    return jsonify(resultado), 200

@app.route("/validar_datos", methods=["POST"])
def validar_datos_endpoint():
    """
    Endpoint que valida un conjunto de datos personales.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Debe enviar un cuerpo JSON válido"}), 400

    resultado = validar_con_tiempo(data)
    return jsonify(resultado), 200

@app.route("/verificar_externo", methods=["GET"])
def verificar_externo_endpoint():
    """
    Endpoint que simula una verificación externa usando requests.
    """
    email = request.args.get("email", "demo@correo.com")
    resultado = verificar_en_servicio_externo(email)
    return jsonify(resultado), 200

# ========== NUEVO ENDPOINT PARA FEATURE FLAGS ==========
@app.route("/feature-flags", methods=["GET"])
def get_feature_flags():
    """
    Endpoint para ver el estado de los feature flags para el usuario actual
    """
    user_ip = request.remote_addr or "anonymous"
    
    flags = {
        "user_key": user_ip,
        "feature_flags": {
            "nuevo-mensaje-bienvenida": get_feature_flag(user_ip, 'nuevo-mensaje-bienvenida', False),
            "status-detallado": get_feature_flag(user_ip, 'status-detallado', False),
            "validacion-mejorada": get_feature_flag(user_ip, 'validacion-mejorada', False)
        }
    }
    
    return jsonify(flags), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)