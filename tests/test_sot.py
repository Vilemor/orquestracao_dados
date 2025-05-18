from pipeline.sor_sot import aplicar_tratamentos
import pandas as pd

def test_aplicar_tratamentos():
    df = pd.DataFrame({'nome': ['joão'], 'cpf': ['123.456.789-00']})
    df_trat = aplicar_tratamentos(df)
    assert df_trat['nome'][0] == 'João'
    assert df_trat['cpf'][0] == '12345678900'
