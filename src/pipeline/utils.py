import os
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import from_json, col, explode, trim, isnan
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, DoubleType, IntegerType



_spark_session = None


def get_spark_session(app_name: str = "Pipeline Local CSV → JSON"):
    global _spark_session
    if _spark_session is None:
        _spark_session = SparkSession.builder \
            .appName(app_name) \
            .master("local[*]") \
            .config("spark.sql.shuffle.partitions", "8") \
            .config("spark.driver.memory", "4g") \
            .config("spark.executor.memory", "4g") \
            .config("spark.driver.maxResultSize", "2g") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .config("spark.sql.files.maxPartitionBytes", "64m") \
            .config("spark.sql.autoBroadcastJoinThreshold", "10MB") \
            .getOrCreate()

        _spark_session.sparkContext.setLogLevel("WARN")  # Reduz verbosidade no terminal

    return _spark_session


def stop_spark_session():
    global _spark_session
    if _spark_session:
        _spark_session.stop()
        _spark_session = None


def carregar_dados_brutos_csv(caminho_arquivo: str, spark):
    """Função irá orquestração o carregamento dos dados brutos do CSV para um json."""
    df_dados_bruto = carregar_csv(caminho_arquivo=caminho_arquivo, spark=spark)
    print(df_dados_bruto.count())
    return df_dados_bruto


def carregar_csv(caminho_arquivo: str, spark):
    df = spark.read.options(header='True', inferSchema='True', delimiter=',').csv(caminho_arquivo)
    df.printSchema(5)
    return df


def salvar_dataframe_como_json(df: DataFrame, caminho_saida: str, modo: str = "overwrite") -> None:
    """
    Salva um DataFrame PySpark como arquivo JSON na pasta especificada.

    Parâmetros:
    ----------
    df : pyspark.sql.DataFrame
        O DataFrame que será salvo.
    
    caminho_saida : str
        Caminho do diretório onde os arquivos JSON serão salvos.
        Ex: "./outputs/dados_tratados"
    
    modo : str, opcional
        Modo de salvamento. Pode ser "overwrite", "append", "ignore" ou "errorifexists". Default é "overwrite".

    Retorno:
    -------
    None
    """
    if not isinstance(df, DataFrame):
        raise TypeError("O objeto fornecido não é um DataFrame do PySpark.")
    
    # Garante que o diretório de saída existe se estiver no filesystem local
    if not caminho_saida.startswith("s3://") and not os.path.exists(caminho_saida):
        os.makedirs(caminho_saida, exist_ok=True)

    df.write.mode(modo).json(caminho_saida)


def carregar_e_tratar_json(caminho_pasta: str, spark: SparkSession) -> DataFrame:
    """
    Carrega arquivos JSON de uma pasta e aplica filtros:
      1. `observacoes` não nulo e não vazio.
      2. `salario` não nulo, não NaN e existente.

    Parâmetros:
    ----------
    caminho_pasta : str
        Caminho da pasta onde estão os arquivos JSON (sem nome de arquivo).

    spark : SparkSession
        Sessão Spark ativa.

    Retorno:
    -------
    DataFrame
        DataFrame filtrado e tratado.
    """
    # Carregar todos os arquivos JSON da pasta
    df_bruto = spark.read.json(caminho_pasta)
    print(f"Volume de dados brutos: {df_bruto.count()}")

    # Filtrar onde `observacoes` não é nulo nem vazio (após trim)
    df_obs = df_bruto.filter(col("observacoes").isNotNull() & (trim(col("observacoes")) != ""))
    print(f"Volume de dados tratado observações: {df_obs.count()}")
    
    # Agrupa pelas categorias e conta quantos registros tem em cada uma
    # df_agrupado = df_bruto.groupBy("categoria_cliente").count()
    # print(f"Volume de dados agrupados: {df_agrupado.count()}")
    
    lista_categorias = [row["categoria_cliente"] for row in df_bruto.select("categoria_cliente").distinct().collect()]
    print("Categorias:", lista_categorias)

    # Filtrar onde `salario` é diferente de nulo e não é NaN
    df_salario = df_bruto.filter(col("salario").isNotNull() & (~isnan(col("salario"))))
    print(f"Volume de dados tratado salario: {df_salario.count()}")

    return df_bruto