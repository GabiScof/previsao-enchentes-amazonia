import os
import zipfile
import shutil
import pandas as pd
from src.helpers.formata_csv_clima import formataCSVClima


class extracaoCSV():

    def extracao_csv(self):
        lista_municipios = ['AM', 'AP', 'AC', 'MA', 'MT', 'PA', 'RO', 'RR', 'TO']

        zip_folder = '../../data/brutos/clima/'
        extract_folder_base = '../../data/extracao/temporario/'
        output_folder = '../../data/extracao/anual/'
        os.makedirs(output_folder, exist_ok=True)

        for ano in range(2000, 2026):
            zip_name = f"{ano}.zip"
            zip_path = os.path.join(zip_folder, zip_name)

            if not os.path.exists(zip_path):
                print(f"Arquivo {zip_name} não encontrado.")
                continue

            print(f"\nProcessando {zip_name}...")

            extract_path = os.path.join(extract_folder_base, str(ano))

            # Remove a pasta antiga (se existir) e recria
            if os.path.exists(extract_path):
                shutil.rmtree(extract_path)
            os.makedirs(extract_path, exist_ok=True)

            # Extrai os arquivos
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            dataframes = []

            for root, _, files in os.walk(extract_path):
                for nome_arquivo in files:
                    if nome_arquivo.endswith('.CSV'):
                        caminho_arquivo = os.path.join(root, nome_arquivo)

                        try:
                            with open(caminho_arquivo, 'r', encoding='latin1') as f:
                                linhas = f.readlines()

                            uf = None
                            for linha in linhas:
                                if linha.startswith('UF:;'):
                                    uf = linha.split(';')[1].strip()
                                    break

                            if uf not in lista_municipios:
                                continue

                            partes = nome_arquivo.split('_')
                            municipio = partes[4] if len(partes) >= 5 else 'desconhecido'
                            municipio = municipio.capitalize()

                            df = pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', skiprows=8, engine='python')
                            df['municipio'] = municipio
                            df['estado'] = uf
                            dataframes.append(df)

                        except Exception as e:
                            print(f"Erro ao processar {nome_arquivo}: {e}")

            if dataframes:
                classe = formataCSVClima()
                df_concatenado = pd.concat(dataframes, ignore_index=True)
                output_path = os.path.join(output_folder, f'dados-clima-{ano}.csv')

                #Pré-processamento
                if 'RADIACAO GLOBAL (Kj/m²)' in df_concatenado.columns:
                    df_concatenado.rename(columns={'RADIACAO GLOBAL (Kj/m²)': 'RADIACAO GLOBAL (KJ/m²)'}, inplace=True)

                colunas_para_formatar = ['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)', 'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)', 'PRESSÃO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)', 'PRESSÃO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)', 'RADIACAO GLOBAL (KJ/m²)', 'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)', 'TEMPERATURA DO PONTO DE ORVALHO (°C)', 'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)', 'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)', 'TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (°C)', 'TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (°C)', 'UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)', 'UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)', 'UMIDADE RELATIVA DO AR, HORARIA (%)', 'VENTO, DIREÇÃO HORARIA (gr) (° (gr))', 'VENTO, RAJADA MAXIMA (m/s)', 'VENTO, VELOCIDADE HORARIA (m/s)']
                for coluna in colunas_para_formatar:
                    df_concatenado = classe.remover_valores_invalidos(df=df_concatenado, coluna=coluna)

                df_concatenado = classe.separa_coluna_dia_mes_ano(df=df_concatenado)
                df_concatenado = classe.transforma_numerico(df=df_concatenado, colunas_numericas=colunas_para_formatar)
                df_concatenado = classe.agrupa_por_dia(df=df_concatenado)
                df_concatenado.to_csv(output_path, index=False, sep=';')
                print(f"Dataframe concatenado!")
            else:
                print(f"Nenhum dado válido encontrado para {ano}.")

    def extracao_final(self):
        dataframes = []
        pasta_csv = '../../data/extracao/anual/'

        for arquivo in os.listdir(pasta_csv):
            if arquivo.endswith('.csv'):
                caminho_completo = os.path.join(pasta_csv, arquivo)
                try:
                    df = pd.read_csv(caminho_completo, encoding='latin1', sep=';')
                    dataframes.append(df)
                    print(f"Lido: {arquivo}")
                except Exception as e:
                    print(f"Erro ao ler {arquivo}: {e}")

        if dataframes:
            print(f"Iniciando concatenação dos arquivos")
            df_final = pd.concat(dataframes, ignore_index=True)
            output_path_final = '../../data/extracao/dados-clima-diario-final.csv'
            df_final.to_csv(output_path_final, index=False, sep=';')
            print(f"Arquivo final gerado com sucesso: {output_path_final}")
        else:
            print("Nenhum CSV foi lido para gerar o arquivo final.")
