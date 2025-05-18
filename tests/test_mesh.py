from pipeline.sot_mesh import gerar_json
import pandas as pd

def test_gerar_json():
    df = pd.DataFrame([{'nome': 'João', 'cpf': '12345678900', 'idade': 30}])
    json_str = gerar_json(df)
    assert '"nome": "João"' in json_str
