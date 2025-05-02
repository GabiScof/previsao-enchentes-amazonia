import pandas as pd

from src.helpers.formata_csv import formataCSV
from src.helpers.pre_processamento import PreProcessamento

if __name__ == "__main__":
    print(f"\nIniciando agrupamento  formatação dos dados!")
    classe = formataCSV()

    print(f"\nInciciando leitura dos dados")
    # Leitura dos dataframe de pluviometria, municipio e desmatamento
    df_ap = pd.read_csv('../../data/brutos/dados-pluviometricos-AP.csv')
    df_ac = pd.read_csv('../../data/brutos/dados-pluviometricos-AC.csv')
    df_ma = pd.read_csv('../../data/brutos/dados-pluviometricos-MA.csv')
    df_ro = pd.read_csv('../../data/brutos/dados-pluviometricos-RO.csv')
    df_rr = pd.read_csv('../../data/brutos/dados-pluviometricos-RR.csv')
    df_vazao_ac = pd.read_csv('../../data/brutos/dados-vazao-AC.csv')
    df_vazao_am = pd.read_csv('../../data/brutos/dados-vazao-AM.csv')
    df_vazao_ap = pd.read_csv('../../data/brutos/dados-vazao-AP.csv')
    df_vazao_ma = pd.read_csv('../../data/brutos/dados-vazao-MA.csv')
    df_vazao_mt = pd.read_csv('../../data/brutos/dados-vazao-MT.csv')
    df_vazao_pa = pd.read_csv('../../data/brutos/dados-vazao-PA.csv')
    df_vazao_ro = pd.read_csv('../../data/brutos/dados-vazao-RO.csv')
    df_vazao_rr = pd.read_csv('../../data/brutos/dados-vazao-RR.csv')
    df_vazao_to = pd.read_csv('../../data/brutos/dados-vazao-TO.csv')
    df_municipios = pd.read_csv('../../data/brutos/estacao-pluviometrica-municipio.csv')
    df_municipios_vazao = pd.read_csv('../../data/brutos/estacao-vazao-municipio.csv')
    df_desmatamento= pd.read_csv('../../data/brutos/desmatamento_por_municipio.csv')
    df_desmatamento_datazoom= pd.read_csv('../../data/brutos/mapbiomas_muni_deforestation_regeneration.csv',  sep=';')
    df_clima = pd.read_csv('../../data/extracao/dados-clima-diario-final.csv', encoding='latin1', sep=';', engine='python')

    # DADOS DE PLUVIOMETRIA -----------------------------------------------------------------------------------
    print(f"Inciciando tratamento dos dados de pluviometria")
    # Criação do dataframe de pluviometria com todos os estados
    lista_dfs = [df_ap,df_ac, df_ma, df_ro,df_rr]
    df_pluviometria = classe.concatena_df(lista_dfs=lista_dfs)

    # Pré-processamento de colunas
    df_pluviometria = classe.separa_coluna_data(df=df_pluviometria)

    # Agrupamento dos dataframes de código de município e nome de município
    df_pluviometria = classe.merge_codigo_municipio(df_codigos=df_pluviometria, df_municipios=df_municipios)
    df_pluviometria = df_pluviometria.drop(columns=['estacao','codigo_estacao'])
    df_pluviometria = classe.agrupa_por_media(df=df_pluviometria, coluna='chuva' , condicao=['dia','mes','ano','municipio','uf'])


    # DADOS DE VAZÃO -----------------------------------------------------------------------------------
    print(f"Inciciando tratamento dos dados de vazão")
    # Criação do dataframe de pluviometria com todos os estados
    lista_dfs_vazao = [df_vazao_am,df_vazao_ac,df_vazao_mt,df_vazao_ap,df_vazao_ma,df_vazao_ro,df_vazao_rr,df_vazao_pa,df_vazao_to]
    df_vazao = classe.concatena_df(lista_dfs=lista_dfs_vazao)

    # Pré-processamento de colunas
    df_vazao = classe.separa_coluna_data(df=df_vazao)

    # Agrupamento dos dataframes de código de município e nome de município
    df_vazao = classe.merge_codigo_municipio(df_codigos=df_vazao, df_municipios=df_municipios_vazao)
    df_vazao = df_vazao.drop(columns=['estacao','codigo_estacao'])
    df_vazao = classe.agrupa_por_media(df=df_vazao, coluna='vazao' , condicao=['dia','mes','ano','municipio','uf'])

    # TODOS OS DATAFRAMES -----------------------------------------------------------------------------------
    print(f"Iniciando pré-processamento de todos os dataframes")
    # Pré-processamento de strings
    df_pluviometria['municipio'] = df_pluviometria['municipio'].apply(classe.formata_string)
    df_desmatamento['municipality'] = df_desmatamento['municipality'].apply(classe.formata_string)
    df_vazao['municipio'] = df_vazao['municipio'].apply(classe.formata_string)
    df_clima['municipio'] = df_clima['municipio'].apply(classe.formata_string)

    # Seleção das colunas do df de desmatamento
    df_desmatamento = df_desmatamento[['year', 'areakm', 'municipality']]
    df_desmatamento_datazoom = df_desmatamento_datazoom[['municipio','uf','cod_municipio','ano','valor','classe_desmatamento']]

    # Renomeação das colunas do df de desmatamento
    df_desmatamento.rename(columns={'year': 'ano', 'municipality': 'municipio'}, inplace=True)

    # Calculo de desmatamento do dataframe do datazoom
    df_desmatamento_datazoom = df_desmatamento_datazoom[df_desmatamento_datazoom['classe_desmatamento'].str.contains('Supressao')]
    df_desmatamento_datazoom = df_desmatamento_datazoom[df_desmatamento_datazoom['ano'] >= 1991]
    df_desmatamento_datazoom['municipio'] = df_desmatamento_datazoom['municipio'].apply(classe.formata_string)
    df_desmatamento_datazoom['valor'] = df_desmatamento_datazoom['valor'].astype(str).str.replace(',', '.').astype(float)
    df_desmatamento_datazoom = df_desmatamento_datazoom.groupby(['ano', 'municipio'])['valor'].sum().reset_index()
    df_desmatamento_datazoom['valor'] = df_desmatamento_datazoom['valor'] / 100

    # Agrupamento dos dataframes de pluviometria, desmatamento e vazão
    df_desma_pluvio = classe.agrupa_csv(df_pluviometria=df_pluviometria, df_desmatamento=df_desmatamento, condicoes=['ano', 'municipio'], modo = 'left')
    df_desma_pluvio = classe.agrupa_csv(df_pluviometria=df_desma_pluvio, df_desmatamento=df_desmatamento_datazoom, condicoes=['ano', 'municipio'], modo = 'left')
    df_desma_pluvio_vazao = classe.agrupa_csv(df_pluviometria=df_desma_pluvio, df_desmatamento=df_vazao, condicoes=['ano', 'mes', 'dia', 'municipio'], modo = 'outer')

    # Preenchimento dos valores de desmatamento nan do dataframe destamamento com o dataframe desmatamento do datazoom
    df_desma_pluvio_vazao['areakm'] = df_desma_pluvio_vazao['areakm'].fillna(df_desma_pluvio_vazao['valor'])

    # Renomeação das colunas
    df_clima.columns = [classe.limpar_nome_coluna(c) for c in df_clima.columns]
    df_clima.rename(columns={
        "PRECIPITAAAAAO TOTAL, HORAARIO (mm)": "precipitacao_total_mm",
        "PRESSAAO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)": "pressao_max_ant_mb",
        "PRESSAAO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)": "pressao_min_ant_mb",
        "RADIACAO GLOBAL (KJ/mAA2)": "radiacao_global_kj_m2",
        "TEMPERATURA DO AR - BULBO SECO, HORARIA (AAC)": "temperatura_bulbo_seco_c",
        "TEMPERATURA DO PONTO DE ORVALHO (AAC)": "temperatura_orvalho_c",
        "TEMPERATURA MAAXIMA NA HORA ANT. (AUT) (AAC)": "temperatura_max_ant_c",
        "TEMPERATURA MAANIMA NA HORA ANT. (AUT) (AAC)": "temperatura_min_ant_c",
        "TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (AAC)": "orvalho_max_ant_c",
        "TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (AAC)": "orvalho_min_ant_c",
        "umidade_max_ant_pct": "umidade_max_ant_pct",
        "umidade_min_ant_pct": "umidade_min_ant_pct",
        "umidade_ar_pct": "umidade_ar_pct",
        "VENTO, DIREAAAAO HORARIA (gr) (AA (gr))": "vento_direcao_graus",
        "vento_rajada_max_ms": "vento_rajada_max_ms",
        "vento_velocidade_ms": "vento_velocidade_ms",
        "PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)": "pressao_nivel_estacao_mb",
        "UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)": "umidade_max_ant_pct",
        "UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)": "umidade_min_ant_pct",
        "UMIDADE RELATIVA DO AR, HORARIA (%)": "umidade_ar_pct",
        "VENTO, RAJADA MAXIMA (m/s)": "vento_rajada_max_ms",
        "VENTO, VELOCIDADE HORARIA (m/s)": "vento_velocidade_ms",
    }, inplace=True)

    # Remover coluna desnecessária
    df_clima = df_clima.drop(columns = ['Unnamed: 19'])

    # Agrupamento dos dataframes de pluviometria-desmatamento e clima
    df_desma_pluvio_vazao_clima = classe.agrupa_csv(df_pluviometria=df_desma_pluvio_vazao, df_desmatamento=df_clima, condicoes=['ano', 'mes','dia', 'municipio'], modo='left')
    df_desma_pluvio_vazao_clima['chuva_final'] = df_desma_pluvio_vazao_clima['precipitacao_total_mm'].combine_first(df_desma_pluvio_vazao_clima['chuva'])

    # Retirar colunas desnecessárias
    df_desma_pluvio_vazao_clima = df_desma_pluvio_vazao_clima.drop(columns = ['chuva', 'precipitacao_total_mm', 'estado','valor'])

    # Preenchimento dados faltantes de desmatamento
    print(f"Iniciando preenchimento dos dados faltantes de desmatamento.")
    preprocessamento = PreProcessamento()

    # Preenchimento por média mensal do município
    media_mes_desmatamento = df_desma_pluvio_vazao_clima.groupby(['ano', 'mes', 'municipio'])['areakm'].mean().reset_index()
    df_merge = df_desma_pluvio_vazao_clima.merge(media_mes_desmatamento,on=['ano', 'mes', 'municipio'],how='left',suffixes=('', '_media'))
    df_merge['areakm'] = df_merge['areakm'].fillna(df_merge['areakm_media'])
    df_merge.drop(columns=['areakm_media'], inplace=True)
    df_desma_pluvio_vazao_clima = df_merge

    # Preenchimento por média anual do município
    media_ano_desmatamento = df_desma_pluvio_vazao_clima.groupby(['ano', 'municipio'])['areakm'].mean().reset_index()
    df_merge = df_desma_pluvio_vazao_clima.merge(media_ano_desmatamento,on=['ano', 'municipio'],how='left',suffixes=('', '_media'))
    df_merge['areakm'] = df_merge['areakm'].fillna(df_merge['areakm_media'])
    df_merge.drop(columns=['areakm_media'], inplace=True)
    df_desma_pluvio_vazao_clima = df_merge

    # Preenchimento por média anual
    media_ano_desmatamento_tot = df_desma_pluvio_vazao_clima.groupby(['ano'])['areakm'].mean().reset_index()
    df_merge = df_desma_pluvio_vazao_clima.merge(media_ano_desmatamento_tot,on=['ano'],how='left',suffixes=('', '_media'))
    df_merge['areakm'] = df_merge['areakm'].fillna(df_merge['areakm_media'])
    df_merge.drop(columns=['areakm_media'], inplace=True)
    df_desma_pluvio_vazao_clima = df_merge

    print(f"O dataset possui {df_desma_pluvio_vazao_clima['areakm'].isna().sum()} linhas onde 'areakm' eh nan.")

    df_desma_pluvio_vazao_clima.to_csv('../../data/formatados/dados-pluviometricos-vazao-desmatamento-clima.csv', index=False)

    lista_de_municipios = ['manaus', 'rio branco']
    for municipio in lista_de_municipios:
        df_temp = df_desma_pluvio_vazao_clima[df_desma_pluvio_vazao_clima['municipio'] == municipio]
        df_temp.to_csv(f'../../data/formatados/municipios/dados-{municipio}.csv', index=False)