import pandas as pd

class PreProcessamento:
    def preencher_dados(self, media, row, coluna: str, coluna_media: str):
        if pd.notna(row[coluna]):
            return row[coluna]

        media = media[media[coluna_media] == row[coluna_media]]
        media_selecao = media[media[coluna].notna()]
        if media_selecao.empty:
            return row[coluna]

        media_selecao['diferenca_ano'] = (media_selecao['ano'] - row['ano']).abs()
        media_mais_proxima = media_selecao.sort_values('diferenca_ano').iloc[0][coluna]
        return media_mais_proxima

