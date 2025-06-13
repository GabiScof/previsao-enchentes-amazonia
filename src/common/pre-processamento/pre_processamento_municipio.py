import pandas as pd
import os
from src.helpers.pre_processamento import PreProcessamento

if __name__ == "__main__":
    # Caminho para a pasta com os arquivos dos municípios
    pasta_csvs = '../../data/formatados/municipios'
    saida_completa = '../../data/pre-processados/completo'
    saida_sem_clima = '../../data/pre-processados/sem_clima'

    # Cria as pastas de saída se não existirem
    os.makedirs(saida_completa, exist_ok=True)
    os.makedirs(saida_sem_clima, exist_ok=True)

    # Inicializa o objeto de pré-processamento
    preprocessamento = PreProcessamento()

    # Itera sobre os arquivos CSV da pasta
    for arquivo in os.listdir(pasta_csvs):
        if arquivo.endswith('.csv'):
            caminho_csv = os.path.join(pasta_csvs, arquivo)
            print(f"\n🔹 Processando arquivo: {arquivo}")
            df = pd.read_csv(caminho_csv)

        # Compreensão da distribuição dos dados do dataset
        print(f"\nANTES DE PRÉ-PROCESSAR:\nO dataset possui {len(df)} linhas.\n")
        print(f"INICIANDO PRÉ-PROCESSAMENTO:")

        # Pré-processamento da coluna uf
        df['uf'] = df['uf_x'].fillna(df['uf_y'])
        df.drop(columns=['uf_x', 'uf_y'], inplace=True)

        # Agrupamento das linhas repetidas
        df = df.groupby(['ano', 'mes','dia','municipio','uf'])[['chuva_final', 'vazao', 'areakm','pressao_nivel_estacao_mb','pressao_max_ant_mb','pressao_min_ant_mb','radiacao_global_kj_m2','temperatura_bulbo_seco_c','temperatura_orvalho_c','temperatura_max_ant_c','temperatura_min_ant_c','orvalho_max_ant_c','orvalho_min_ant_c','umidade_max_ant_pct','umidade_min_ant_pct','umidade_ar_pct','vento_direcao_graus','vento_rajada_max_ms','vento_velocidade_ms']].mean().reset_index()

        # Ajuste da coluna de desmatamento para diário
        df.loc[df['areakm'].notna(), 'areakm'] = df['areakm'] / 365

        # Pré-processamento dos valores nan das colunas de dados: vazão, chuva e desmatamento

        # Preenchimento dos nan pela média da coluna daquele municipio no ano mais próximo ao da linha faltante
        colunas = ['chuva_final','vazao','areakm','pressao_nivel_estacao_mb','pressao_max_ant_mb','pressao_min_ant_mb','radiacao_global_kj_m2','temperatura_bulbo_seco_c','temperatura_orvalho_c','temperatura_max_ant_c','temperatura_min_ant_c','orvalho_max_ant_c','orvalho_min_ant_c','umidade_max_ant_pct','umidade_min_ant_pct','umidade_ar_pct','vento_direcao_graus','vento_rajada_max_ms','vento_velocidade_ms']
        print(f"\nIniciando preenchendo dados por mes e ano e município:")
        for coluna in colunas:
            print(f"  * coluna {coluna}")
            media_mes = df.groupby(['ano','mes', 'municipio'])[coluna].mean().reset_index()
            df[coluna] = df.apply(lambda row: preprocessamento.preencher_dados(media=media_mes, row=row, coluna=coluna,coluna_media='municipio'), axis=1)

        # Preenchimento dos nan pela média da coluna daquele municipio no ano mais próximo ao da linha faltante
        print(f"\nIniciando preenchendo dados por ano e municipio:")
        for coluna in colunas:
            print(f"  * coluna {coluna}")
            media_mes = df.groupby(['ano', 'municipio'])[coluna].mean().reset_index()
            df[coluna] = df.apply(lambda row: preprocessamento.preencher_dados(media=media_mes, row=row, coluna=coluna,coluna_media='municipio'), axis=1)

        # Preenchimento dos nan pela média da coluna daquela uf no ano mais próximo ao da linha faltante
        print(f"\nIniciando preenchendo dados por ano e uf:")
        for coluna in colunas:
            print(f"  * coluna {coluna}")
            media_mes = df.groupby(['ano', 'uf'])[coluna].mean().reset_index()
            df[coluna] = df.apply(lambda row: preprocessamento.preencher_dados(media=media_mes, row=row, coluna=coluna,coluna_media='uf'), axis=1)

        # Preenchimento dos nan pela média da coluna daquele ano
        print(f"\nIniciando preenchendo dados por media por ano:")
        print(f"  * coluna desmatamento\n")
        media_ano_desmatamento_tot = df.groupby(['ano'])['areakm'].mean().reset_index()
        df['areakm'] = df.apply(lambda row: preprocessamento.preencher_dados(media=media_ano_desmatamento_tot, row=row, coluna='areakm', coluna_media='ano'), axis=1)

        # Nome base sem extensão
        nome_base = os.path.splitext(arquivo)[0]
        df.to_csv(os.path.join(saida_completa, f"{nome_base}-preprocessado.csv"), index=False)

        # Compreensão da distribuição dos dados do dataset
        print(f"DEPOIS DE PRÉ-PROCESSAR:\nO dataset possui {len(df)} linhas.")
        print(f"O dataset possui {df['pressao_nivel_estacao_mb'].isna().sum()} linhas onde 'pressao_nivel_estacao_mb' eh nan.")
        print(f"O dataset possui {df['areakm'].isna().sum()} linhas onde 'areakm' eh nan.")
        print(f"O dataset possui {df['chuva_final'].isna().sum()} linhas onde 'chuva_final' eh nan.")
        print(f"O dataset possui {df['vazao'].isna().sum()} linhas onde 'vazao' eh nan.")

        df_sem_clima = df.drop(columns = ['pressao_nivel_estacao_mb','pressao_max_ant_mb','pressao_min_ant_mb','radiacao_global_kj_m2','temperatura_bulbo_seco_c','temperatura_orvalho_c','temperatura_max_ant_c','temperatura_min_ant_c','orvalho_max_ant_c','orvalho_min_ant_c','umidade_max_ant_pct','umidade_min_ant_pct','umidade_ar_pct','vento_direcao_graus','vento_rajada_max_ms','vento_velocidade_ms'])
        df_sem_clima.to_csv(os.path.join(saida_sem_clima, f"{nome_base}-sem-clima.csv"), index=False)
