import json
from app.api import app

def test_validar_endpoint():
    cliente = app.test_client()
    resp = cliente.post('/validar', json={'cedula': '1710034065'})
    data = json.loads(resp.data)
    assert resp.status_code == 200
    assert data['valida'] is True
