import utils


if __name__:
    spark = utils.get_spark_session()
    df_dados_brutos = utils.carregar_dados_brutos_csv("data/dados_brutos.csv", spark)
    utils.salvar_dataframe_como_json(df_dados_brutos, 'outputs/dados_brutos')
    utils.stop_spark_session()