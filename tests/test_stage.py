from src.pipeline.stage import ler_csv_stage

def test_ler_csv_stage():
    df = ler_csv_stage("data/dados.csv")
    assert not df.empty
