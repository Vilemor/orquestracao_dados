from pipeline.stage_sor import padronizar_dados
import pandas as pd

def test_padronizar_dados():
    df = pd.DataFrame({' Nome ': ['João'], 'Idade ': [30]})
    df_pad = padronizar_dados(df)
    assert list(df_pad.columns) == ['nome', 'idade']
