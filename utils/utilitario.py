from typing import Optional

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import (
    StructType, StructField, IntegerType, StringType, DoubleType,
    BooleanType, DateType, TimestampType
)
from pyspark.sql.functions import col
from utils.json_logger import log_json

_spark_session: Optional[SparkSession] = None


def get_spark_session(app_name: str = "Pipeline Local") -> SparkSession:
    """
    Inicializa e retorna uma instância singleton do SparkSession.
    """
    global _spark_session
    try:
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
            _spark_session.sparkContext.setLogLevel("WARN")
            log_json("SparkSession inicializada com sucesso.")
        else:
            log_json("SparkSession já existente, reutilizando instância.")
        return _spark_session
    except Exception as e:
        log_json(f"Erro ao inicializar SparkSession: {str(e)}", level="ERROR")
        raise


def stop_spark_session() -> None:
    """
    Encerra a instância global do SparkSession, se existir.
    """
    global _spark_session
    try:
        if _spark_session:
            _spark_session.stop()
            _spark_session = None
            log_json("SparkSession finalizada com sucesso.")
        else:
            log_json("Nenhuma SparkSession ativa para finalizar.", level="WARNING")
    except Exception as e:
        log_json(f"Erro ao finalizar SparkSession: {str(e)}", level="ERROR")
        raise


def schema_csv() -> StructType:
    """
    Retorna o schema padrão para o DataFrame de clientes.
    """
    return StructType([
        StructField("id", IntegerType(), True),
        StructField("nome", StringType(), True),
        StructField("email", StringType(), True),
        StructField("data_nascimento", DateType(), True),
        StructField("cpf", StringType(), True),
        StructField("telefone", StringType(), True),
        StructField("salario", DoubleType(), True),
        StructField("ativo", BooleanType(), True),
        StructField("ultima_compra", TimestampType(), True),
        StructField("categoria_cliente", StringType(), True),
        StructField("observacoes", StringType(), True),
    ])


def normalizar_dataframe(df: DataFrame) -> DataFrame:
    """
    Normaliza os tipos de dados do DataFrame conforme o schema definido.

    Args:
        df (DataFrame): DataFrame de entrada.

    Returns:
        DataFrame: DataFrame com colunas convertidas para os tipos corretos.
    """
    try:
        schema = schema_csv()
        for field in schema.fields:
            df = df.withColumn(field.name, col(field.name).cast(field.dataType))
        log_json("DataFrame normalizado com sucesso.")
        return df
    except Exception as e:
        log_json(f"Erro ao normalizar DataFrame: {str(e)}", level="ERROR")
        raise


def salvar_dataframe_como_parquet(df: DataFrame, caminho_saida: str) -> None:
    """
    Salva o DataFrame em formato Parquet no caminho especificado.

    Args:
        df (DataFrame): DataFrame a ser salvo.
        caminho_saida (str): Caminho de saída para o arquivo Parquet.
    """
    try:
        df.coalesce(1).write.mode("overwrite").parquet(caminho_saida)
        log_json(f"DataFrame salvo como Parquet em '{caminho_saida}'.")
    except Exception as e:
        log_json(f"Erro ao salvar DataFrame como Parquet: {str(e)}", level="ERROR")
        raise
