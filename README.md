# orquestracao_dados
repositório de treinamento para orquestração e manipulação de dados com pysark

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("ReprocessamentoAcumulado").getOrCreate()

# Dados do histórico (df_sor)
dados_historico = [
    (1, '2025-08-01', 5, '2025-08-01'),
    (1, '2025-08-02', 10, '2025-08-02'),
    (1, '2025-08-03', 20, '2025-08-03'),
]
df_sor = spark.createDataFrame(dados_historico, ["id_produto", "data", "qtd", "data_processamento"])

# Novo dado corrigido (df_staging)
dados_staging = [
    (1, '2025-08-01', 20, '2025-08-06'),
]
df_staging = spark.createDataFrame(dados_staging, ["id_produto", "data", "qtd", "data_processamento"])

# Junta as chaves afetadas
chaves_afetadas = df_staging.select("id_produto").distinct()

# Filtra histórico afetado
historico_afetado = df_sor.join(chaves_afetadas, on="id_produto", how="inner")

# Junta os dois conjuntos
df_ajustado = historico_afetado.unionByName(df_staging)

# Remove duplicidades mantendo o mais novo por data
janela_rank = Window.partitionBy("id_produto", "data").orderBy(desc("data_processamento"))
df_sem_duplicidade = df_ajustado.withColumn("rank", row_number().over(janela_rank)).filter(col("rank") == 1).drop("rank")

# Ordena por data e calcula acumulado
janela_acumulado = Window.partitionBy("id_produto").orderBy("data")
df_resultado = df_sem_duplicidade.withColumn("total_acumulado", sum("qtd").over(janela_acumulado))

# Mostra resultado
df_resultado.orderBy("data").show(truncate=False)
```