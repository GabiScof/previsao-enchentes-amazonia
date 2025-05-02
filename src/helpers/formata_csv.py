from typing import Union
import pandas as pd
import unicodedata
from pandas import DataFrame

class formataCSV:

    def separa_coluna_data(self,df:DataFrame):

        df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d', errors='coerce')
        df['ano'] = df['data'].dt.year
        df['mes'] = df['data'].dt.month
        df['dia'] = df['data'].dt.day

        df.drop(columns=['data'], inplace=True)

        return df

    def separa_coluna_dia_mes_ano(self,df:DataFrame):
        df.columns = df.columns.str.lower()
        coluna_data = [col for col in df.columns if 'data' in col][0]

        df['data'] = pd.to_datetime(df[coluna_data], format='%Y-%m-%d', errors='coerce')
        df['ano'] = df['data'].dt.year
        df['mes'] = df['data'].dt.month
        df['dia'] = df['data'].dt.day

        df.drop(columns=['data'], inplace=True)

        return df

    def agrupa_por_mes(self,df:DataFrame, coluna: str):
        df = df.groupby(['ano', 'mes', 'estacao'], as_index=False)[coluna].mean()
        return df

    def agrupa_por_media(self,df:DataFrame, coluna: Union[str, list[str]], condicao: list):
        df = df.groupby(condicao, as_index=False)[coluna].mean()
        return df

    def merge_codigo_municipio(self,df_codigos:DataFrame, df_municipios: DataFrame):
        df = pd.merge(
            df_codigos,
            df_municipios,
            left_on='estacao',
            right_on='codigo_estacao',
            how='left'
        )
        return df

    def agrupa_csv(self,df_pluviometria:DataFrame, df_desmatamento: DataFrame, condicoes: list, modo: str):

        df = pd.merge(
            df_pluviometria,
            df_desmatamento,
            on= condicoes,
            how= modo
        )
        return df

    def formata_string(self, string: str):
        if isinstance(string, str):
            string = str(string).strip().lower()
            string = unicodedata.normalize('NFD', string)
            string = ''.join(c for c in string if unicodedata.category(c) != 'Mn')  # Remove acentos
        return string

    def concatena_df(self,lista_dfs: list):
        df = pd.concat(lista_dfs, ignore_index=True)
        return df

    def limpar_nome_coluna(self, col: str):
        col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf-8')  # remove acentos
        col = col.strip()
        return col