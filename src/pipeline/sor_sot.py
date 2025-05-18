import utils


if __name__ == "__main__":
    spark = utils.get_spark_session()
    df_tratado = utils.carregar_e_tratar_json("outputs/dados_brutos", spark)
    df_tratado.show(truncate=False)
    utils.stop_spark_session()
