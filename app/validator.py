import logging
import time
import requests

# Configuración del log
logging.basicConfig(filename='logs/validator.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def validar_cedula(cedula: str) -> dict:
    """Valida una cédula ecuatoriana con controles adicionales y devuelve un dict con detalles."""
    info = {"cedula": cedula, "valida": False, "tipo": None, "errores": []}

    if not cedula.isdigit() or len(cedula) != 10:
        info["errores"].append("Debe contener exactamente 10 dígitos numéricos.")
        return info

    provincia = int(cedula[:2])
    if not 1 <= provincia <= 24:
        info["errores"].append("Código de provincia inválido (01-24).")
        return info

    tercer = int(cedula[2])
    if tercer >= 6:
        info["tipo"] = "jurídica/extranjero"
        info["errores"].append("No corresponde a persona natural.")
        return info

    digitos = [int(x) for x in cedula]
    total = 0
    for i in range(9):
        valor = digitos[i] * 2 if i % 2 == 0 else digitos[i]
        if valor > 9:
            valor -= 9
        total += valor

    verificador = (10 - (total % 10)) % 10
    if verificador == digitos[-1]:
        info["valida"] = True
        info["tipo"] = "natural"
    else:
        info["errores"].append("Dígito verificador incorrecto.")

    return info


def validar_con_tiempo(cedula: str):
    """Valida una cédula midiendo el tiempo de ejecución y registrando logs."""
    inicio = time.perf_counter()
    try:
        resultado = validar_cedula(cedula)
        duracion = round(time.perf_counter() - inicio, 6)
        resultado["tiempo_validacion"] = f"{duracion} s"
        logging.info(f"Validación ejecutada correctamente: {resultado}")
        return resultado
    except Exception as e:
        logging.error(f"Error validando {cedula}: {e}")
        return {"cedula": cedula, "valida": False, "error": str(e)}


def verificar_en_servicio_externo(cedula: str) -> dict:
    """Simula la verificación de cédula contra un servicio externo."""
    try:
        resp = requests.get(f"https://jsonplaceholder.typicode.com/users/{cedula[-1]}")
        if resp.status_code == 200:
            data = resp.json()
            return {"nombre_simulado": data.get("name"), "fuente": "servicio_externo"}
        return {"error": "No se pudo verificar en servicio externo"}
    except requests.RequestException:
        return {"error": "Error al conectar con el servicio externo"}
