def validar_cedula(cedula: str) -> bool:
    if not cedula.isdigit() or len(cedula) != 10:
        return False

    provincia = int(cedula[:2])
    if provincia < 1 or provincia > 24:
        return False

    digitos = list(map(int, cedula))
    total = 0

    for i in range(9):
        valor = digitos[i] * 2 if i % 2 == 0 else digitos[i]
        if valor > 9:
            valor -= 9
        total += valor

    verificador = (10 - (total % 10)) % 10
    return verificador == digitos[-1]