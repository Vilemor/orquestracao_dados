from src.pipeline.stage import ler_csv_stage
from pipeline.stage_sor import padronizar_dados
from pipeline.sor_sot import aplicar_tratamentos
from pipeline.sot_mesh import gerar_json

def test_pipeline_end_to_end():
    df_stage = ler_csv_stage("data/dados.csv")
    df_sor = padronizar_dados(df_stage)
    df_sot = aplicar_tratamentos(df_sor)
    json_result = gerar_json(df_sot)
    assert "João Silva" in json_result
