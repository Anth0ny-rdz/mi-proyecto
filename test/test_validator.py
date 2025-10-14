from app.validator import validar_cedula
from app.utils import get_status

def test_conexion():
    assert get_status() == "connected"

def test_cedula_valida():
    assert validar_cedula("1710034065") is True

def test_cedula_invalida():
    assert validar_cedula("1710034064") is False

def test_cedula_mal_formato():
    assert validar_cedula("abc") is False