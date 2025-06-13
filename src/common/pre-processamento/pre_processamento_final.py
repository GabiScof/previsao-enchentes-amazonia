import pandas as pd

from src.helpers.pre_processamento import PreProcessamento

if __name__ == "__main__":
    preprocessamento = PreProcessamento()
    df = pd.read_csv('../../data/formatados/dados-pluviometricos-vazao-desmatamento-clima.csv')

    # Compreensão da distribuição dos dados do dataset
    print(f"\nANTES DE PRÉ-PROCESSAR:\nO dataset possui {len(df)} linhas.\n")
    print(f"INICIANDO PRÉ-PROCESSAMENTO:")

    # Pré-processamento da coluna uf
    df['uf'] = df['uf_x'].fillna(df['uf_y'])
    df.drop(columns=['uf_x', 'uf_y', 'estado','valor'], inplace=True)

    # Agrupamento das linhas repetidas
    df = df.groupby(['ano', 'mes', 'municipio','uf'])[['chuva_final', 'vazao', 'areakm','pressao_nivel_estacao_mb','pressao_max_ant_mb','pressao_min_ant_mb','radiacao_global_kj_m2','temperatura_bulbo_seco_c','temperatura_orvalho_c','temperatura_max_ant_c','temperatura_min_ant_c','orvalho_max_ant_c','orvalho_min_ant_c','umidade_max_ant_pct','umidade_min_ant_pct','umidade_ar_pct','vento_direcao_graus','vento_rajada_max_ms','vento_velocidade_ms']].mean().reset_index()

    # Pré-processamento dos valores nan das colunas de dados: vazão, chuva e desmatamento

    # Preenchimento dos nan pela média da coluna daquele municipio no ano mais próximo ao da linha faltante
    media_ano_chuva = df.groupby(['ano', 'municipio'])['chuva_final'].mean().reset_index()
    media_ano_vazao = df.groupby(['ano', 'municipio'])['vazao'].mean().reset_index()
    media_ano_desmatamento = df.groupby(['ano', 'municipio'])['areakm'].mean().reset_index()

    print(f"Iniciando preenchendo dados por media por ano e municipio:")
    print(f"  * coluna chuva")
    df['chuva_final'] = df.apply(lambda row: preprocessamento.preencher_dados(media=media_ano_chuva, row=row, coluna='chuva_final', coluna_media='municipio'), axis=1)
    print(f"  * coluna vazão")
    df['vazao'] = df.apply(lambda row: preprocessamento.preencher_dados(media=media_ano_vazao, row=row, coluna='vazao', coluna_media='municipio'), axis=1)
    print(f"  * coluna desmatamento\n")
    df['areakm'] = df.apply(lambda row: preprocessamento.preencher_dados(media=media_ano_desmatamento, row=row, coluna='areakm', coluna_media='municipio'), axis=1)

    # Preenchimento dos nan pela média da coluna daquela uf no ano mais próximo ao da linha faltante
    media_ano_chuva_estado = df.groupby(['ano', 'uf'])['chuva_final'].mean().reset_index()
    media_ano_vazao_estado = df.groupby(['ano', 'uf'])['vazao'].mean().reset_index()
    media_ano_desmatamento_estado = df.groupby(['ano', 'uf'])['areakm'].mean().reset_index()

    print(f"Iniciando preenchendo dados por media por ano e estado:")
    print(f"  * coluna chuva")
    df['chuva_final'] = df.apply(lambda row: preprocessamento.preencher_dados(media=media_ano_chuva_estado, row=row, coluna='chuva_final', coluna_media='uf'), axis=1)
    print(f"  * coluna vazão")
    df['vazao'] = df.apply(lambda row: preprocessamento.preencher_dados(media=media_ano_vazao_estado, row=row, coluna='vazao', coluna_media='uf'), axis=1)
    print(f"  * coluna desmatamento\n")
    df['areakm'] = df.apply(lambda row: preprocessamento.preencher_dados(media=media_ano_desmatamento_estado, row=row, coluna='areakm', coluna_media='uf'), axis=1)

    # Preenchimento dos nan pela média da coluna daquele ano
    print(f"Iniciando preenchendo dados por media por ano:")
    print(f"  * coluna desmatamento\n")
    media_ano_desmatamento_tot = df.groupby(['ano'])['areakm'].mean().reset_index()
    df['areakm'] = df.apply(lambda row: preprocessamento.preencher_dados(media=media_ano_desmatamento_tot, row=row, coluna='areakm', coluna_media='ano'), axis=1)

    df.to_csv('../../data/pre-processados/dados-finais.csv', index=False)

    # Compreensão da distribuição dos dados do dataset
    print(f"DEPOIS DE PRÉ-PROCESSAR:\nO dataset possui {len(df)} linhas.")
    print(f"O dataset possui {df['pressao_nivel_estacao_mb'].isna().sum()} linhas onde 'pressao_nivel_estacao_mb' eh nan.")
    print(f"O dataset possui {df['areakm'].isna().sum()} linhas onde 'areakm' eh nan.")
    print(f"O dataset possui {df['chuva_final'].isna().sum()} linhas onde 'chuva_final' eh nan.")
    print(f"O dataset possui {df['vazao'].isna().sum()} linhas onde 'vazao' eh nan.")

    df_sem_clima = df.drop(columns = ['pressao_nivel_estacao_mb','pressao_max_ant_mb','pressao_min_ant_mb','radiacao_global_kj_m2','temperatura_bulbo_seco_c','temperatura_orvalho_c','temperatura_max_ant_c','temperatura_min_ant_c','orvalho_max_ant_c','orvalho_min_ant_c','umidade_max_ant_pct','umidade_min_ant_pct','umidade_ar_pct','vento_direcao_graus','vento_rajada_max_ms','vento_velocidade_ms'])
    df_sem_clima.to_csv('../../data/pre-processados/dados-sem-clima-finais.csv', index=False)
