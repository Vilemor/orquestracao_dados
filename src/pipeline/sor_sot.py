import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from utils.utilitario import normalizar_dataframe, get_spark_session, stop_spark_session
from utils.json_logger import log_json


def ler_e_normalizar_parquet(spark, caminho_arquivo_parquet):
    """
    Lê um arquivo .parquet e retorna um DataFrame do PySpark.

    :param spark: SparkSession já inicializada
    :param caminho_arquivo_parquet: str - Caminho completo do arquivo .parquet
    :return: pyspark.sql.DataFrame
    """
    log_json(f"Carregando dados brutos no caminho: {caminho_arquivo_parquet}")
    df = spark.read.parquet(caminho_arquivo_parquet)
    df_normalizado = normalizar_dataframe(df)
    log_json("Dados carregados e normalizados com sucesso.")
    return df_normalizado


if __name__ == "__main__":
    spark = get_spark_session()
    log_json("Iniciando fluxo pipeline SOR -> SOT.")
    df_bruto = ler_e_normalizar_parquet(spark, 'outputs/sor_dado_bruto')
    df_bruto.printSchema()
    df_bruto.show()
    log_json("Finalizando fluxo pipeline SOR -> SOT.")
    stop_spark_session()
