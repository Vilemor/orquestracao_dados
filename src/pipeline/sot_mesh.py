def gerar_json(df, salvar_em=None):
    json_str = df.to_json(orient='records', indent=2, force_ascii=False)
    if salvar_em:
        with open(salvar_em, 'w', encoding='utf-8') as f:
            f.write(json_str)
    return json_str
