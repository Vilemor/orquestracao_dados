from utils.utilitario import (
    get_spark_session,
    stop_spark_session,
    salvar_dataframe_como_parquet,
    schema_csv
)


def carregar_dados_brutos_csv(caminho_arquivo: str, spark, schema):
    """
    Função para carregar dados brutos do csv e converter em um dataframe
    """
    df_dados_brutos = spark.read.options(
        header='True',
        inferSchema='True',
        delimiter=',',
        schema=schema
    ).csv(caminho_arquivo)
    return df_dados_brutos


if __name__:
    spark = get_spark_session()
    schema = schema_csv()
    df_dados_brutos = carregar_dados_brutos_csv(
        caminho_arquivo="data/dados_brutos.csv",
        spark=spark,
        schema=schema
    )
    salvar_dataframe_como_parquet(df_dados_brutos, "outputs/sor_dado_bruto")
    stop_spark_session()
