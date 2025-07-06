import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import dataframe_image as dfi
from geobr import read_municipality
import geopandas as gpd
from unidecode import unidecode

# Pastas
pasta_entrada = '../../data/pre-processados/completo'
pasta_saida = '../../data/analise-dados/por-municipio/distribuicoes2'
os.makedirs(pasta_saida, exist_ok=True)

# Lista de arquivos
arquivos = [f for f in os.listdir(pasta_entrada) if f.endswith('.csv')]

# Pares de variáveis a serem analisadas
pares = [
    ('chuva_final', 'vazao'),
    ('chuva_acumulada_3d', 'vazao'),
    ('chuva_acumulada_14d', 'vazao'),
    ('areakm', 'vazao'),
    ('areakm', 'chuva_acumulada_14d'),
]

# Para cada arquivo...
for arquivo in arquivos:
    caminho_arquivo = os.path.join(pasta_entrada, arquivo)
    df = pd.read_csv(caminho_arquivo)
    df = df.sort_values(['ano', 'mes', 'dia'])

    # Criar colunas de chuva acumulada (se ainda não existirem)
    if 'chuva_acumulada_3d' not in df.columns:
        df['chuva_acumulada_3d'] = df['chuva_final'].rolling(window=3, min_periods=1).sum()
    if 'chuva_acumulada_14d' not in df.columns:
        df['chuva_acumulada_14d'] = df['chuva_final'].rolling(window=14, min_periods=1).sum()

    for x, y in pares:
        if x in df.columns and y in df.columns:
            plt.figure(figsize=(6, 4))
            sns.scatterplot(data=df, x=x, y=y, alpha=0.5)
            plt.title(f'{y} vs {x} – {arquivo}', fontsize=10)
            plt.xlabel(x)
            plt.ylabel(y)
            plt.tight_layout()

            nome_plot = f"{arquivo.replace('.csv', '')}-{y}_vs_{x}.png"
            plt.savefig(os.path.join(pasta_saida, nome_plot))
            plt.close()

            print(f"📌 Gráfico salvo: {nome_plot}")


# # Caminhos
# pasta_entrada = '../../data/pre-processados/completo'
# pasta_saida = '../../data/pre-processados/analise/temporal'
# os.makedirs(pasta_saida, exist_ok=True)

# # Lista de arquivos CSV
# arquivos = [f for f in os.listdir(pasta_entrada) if f.endswith('.csv')]

# # Variáveis de interesse
# variaveis = ['chuva_final', 'vazao', 'areakm']

# # Para cada arquivo
# for arquivo in arquivos:
#     caminho = os.path.join(pasta_entrada, arquivo)
#     df = pd.read_csv(caminho)

#     # Criar coluna de data completa
#     df['data'] = pd.to_datetime(
#         df.rename(columns={'ano': 'year', 'mes': 'month', 'dia': 'day'})[['year', 'month', 'day']])

#     # Ordenar por data
#     df = df.sort_values(by='data')

#     # Agrupar por mês (para suavizar e evitar ruído diário)
#     df_mensal = df.groupby(df['data'].dt.to_period('M'))[variaveis].mean().reset_index()
#     df_mensal['data'] = df_mensal['data'].dt.to_timestamp()

#     for var in variaveis:
#         if var in df_mensal.columns:
#             plt.figure(figsize=(10, 4))
#             plt.plot(df_mensal['data'], df_mensal[var], marker='o', linestyle='-')
#             plt.title(f'Série Temporal de {var} – {arquivo.replace(".csv", "")}')
#             plt.xlabel('Tempo (mensal)')
#             plt.ylabel(var)
#             plt.grid(True)
#             plt.tight_layout()

#             nome_img = f'{arquivo.replace(".csv", "")}-temporal-{var}.png'
#             plt.savefig(os.path.join(pasta_saida, nome_img))
#             plt.close()

#             print(f'📈 Gráfico salvo: {nome_img}')


# # Pastas de entrada e saída
# pasta_entrada = '../../data/pre-processados/completo'
# pasta_saida = '../../data/pre-processados/analise'
# os.makedirs(pasta_saida, exist_ok=True)

# # Lista de arquivos CSV
# arquivos = [f for f in os.listdir(pasta_entrada) if f.endswith('.csv')]

# # Para cada CSV...
# for arquivo in arquivos:
#     caminho_arquivo = os.path.join(pasta_entrada, arquivo)
#     df = pd.read_csv(caminho_arquivo)

#     # Calcula estatísticas
#     estat_desc = df.describe(percentiles=[0.25, 0.5, 0.75])
#     estat_desc.loc['mediana'] = df.median(numeric_only=True)
#     estat_desc.loc['variancia'] = df.var(numeric_only=True)
#     estat_desc.loc['desvio_padrao'] = df.std(numeric_only=True)

#     # Divide as colunas em duas partes
#     metade = len(estat_desc.columns) // 2
#     estat1 = estat_desc.iloc[:, :metade]
#     estat2 = estat_desc.iloc[:, metade:]

#     # Aplica estilo para visualização adequada
#     styled1 = estat1.style.set_table_attributes("style='font-size:9pt'")
#     styled2 = estat2.style.set_table_attributes("style='font-size:9pt'")

#     # Define nomes dos arquivos de imagem
#     nome_base = arquivo.replace('.csv', '')
#     img1 = os.path.join(pasta_saida, f'{nome_base}-estatisticas-parte1.png')
#     img2 = os.path.join(pasta_saida, f'{nome_base}-estatisticas-parte2.png')

#     # Exporta imagens
#     dfi.export(styled1, img1)
#     dfi.export(styled2, img2)

#     print(f"🖼️ Imagens salvas: {img1} e {img2}")

# # Pastas
# pasta_entrada = '../../data/pre-processados/completo'
# pasta_saida = '../../data/pre-processados/analise/distribuicoes'
# os.makedirs(pasta_saida, exist_ok=True)

# # Arquivos CSV
# arquivos = [f for f in os.listdir(pasta_entrada) if f.endswith('.csv')]

# # Para cada arquivo
# for arquivo in arquivos:
#     caminho = os.path.join(pasta_entrada, arquivo)
#     df = pd.read_csv(caminho)

#     df_numerico = df.select_dtypes(include='number')
#     nome_base = arquivo.replace('.csv', '')

#     for coluna in df_numerico.columns:
#         plt.figure(figsize=(8, 4))

#         # Cálculo dos limites com base em quantis (0.5% e 99.5%)
#         q_min = df[coluna].quantile(0.005)
#         q_max = df[coluna].quantile(0.995)

#         # Plot com eixo limitado
#         sns.histplot(df[coluna], kde=True, bins=30, color='skyblue')
#         plt.xlim(q_min, q_max)
#         plt.title(f'Distribuição: {coluna} – {nome_base}', fontsize=10)
#         plt.xlabel(coluna)
#         plt.ylabel('Frequência')
#         plt.tight_layout()

#         # Salvar
#         caminho_img = os.path.join(pasta_saida, f'{nome_base}-{coluna}-distribuicao.png')
#         plt.savefig(caminho_img)
#         plt.close()

#         print(f"📊 Imagem ajustada salva: {caminho_img}")


# # Caminhos
# pasta_entrada = '../../data/pre-processados/completo'
# pasta_saida = '../../data/pre-processados/analise/correlacoes'
# os.makedirs(pasta_saida, exist_ok=True)

# # Arquivos CSV
# arquivos = [f for f in os.listdir(pasta_entrada) if f.endswith('.csv')]

# # Para cada arquivo...
# for arquivo in arquivos:
#     caminho_arquivo = os.path.join(pasta_entrada, arquivo)
#     df = pd.read_csv(caminho_arquivo)

#     # Seleciona apenas colunas numéricas
#     df_numerico = df.select_dtypes(include='number')

#     # Calcula a matriz de correlação de Spearman (recomendada para relações monotônicas e não-lineares)
#     correlacao = df_numerico.corr(method='spearman')

#     # Plota o heatmap
#     plt.figure(figsize=(12, 10))
#     sns.heatmap(correlacao, annot=True, fmt=".2f", cmap='coolwarm', center=0, square=True,
#                 cbar_kws={'label': 'Correlação de Spearman'})
#     plt.title(f'Matriz de Correlação – {arquivo}', fontsize=12)
#     plt.xticks(rotation=45, ha='right')
#     plt.yticks(rotation=0)
#     plt.tight_layout()

#     # Salva imagem
#     nome_base = arquivo.replace('.csv', '')
#     caminho_img = os.path.join(pasta_saida, f'{nome_base}-correlacao.png')
#     plt.savefig(caminho_img)
#     plt.close()

#     print(f"🔥 Heatmap salvo: {caminho_img}")

# # Caminho do arquivo CSV
# arquivo = '../../data/pre-processados/completo/dados-manaus-preprocessado.csv'
# df = pd.read_csv(arquivo)

# # Selecionar somente as colunas desejadas
# colunas = ['areakm', 'chuva_final', 'vazao']
# df_selecionado = df[colunas]

# # Matriz de correlação de Spearman
# matriz_corr = df_selecionado.corr(method='spearman')

# # Plotar heatmap
# plt.figure(figsize=(5, 4))
# sns.heatmap(matriz_corr, annot=True, fmt=".2f", cmap='coolwarm', center=0, square=True,
#             cbar_kws={'label': 'Correlação de Spearman'})
# plt.title('Correlação entre areakm, chuva_final e vazao – Manaus', fontsize=11)
# plt.tight_layout()

# # Salvar imagem (opcional)
# plt.savefig('../../data/pre-processados/analise/correlacao-essenciais-manaus.png')
# plt.show()

# # Caminho do CSV
# arquivo = '../../data/pre-processados/sem_clima/dados-rio branco-sem-clima.csv'
# df = pd.read_csv(arquivo)

# # Ordenar por tempo (importante para rolling)
# df = df.sort_values(by=['ano', 'mes', 'dia'])

# # Calcular chuva acumulada (janela de 3 dias)
# df['chuva_acumulada_3d'] = df['chuva_final'].rolling(window=3, min_periods=1).sum()

# # Selecionar colunas de interesse
# colunas = ['areakm', 'chuva_acumulada_3d', 'vazao']
# df_corr = df[colunas]

# # Calcular matriz de correlação de Spearman
# corr = df_corr.corr(method='spearman')

# # Plotar heatmap
# plt.figure(figsize=(5, 4))
# sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', center=0, square=True,
#             cbar_kws={'label': 'Correlação de Spearman'})
# plt.title('Correlação: chuva acumulada (3 dias), vazão e área – Rio Branco', fontsize=11)
# plt.tight_layout()

# # Salvar imagem
# saida = '../../data/pre-processados/analise/correlacao-janela-chuva-3-Rio Branco.png'
# plt.savefig(saida)
# plt.show()

# print(f"✅ Imagem salva em: {saida}")


# # === CONFIGURAÇÃO ===
# arquivo = '../../data/pre-processados/dados-sem-clima-finais-antigo.csv'
# variaveis = ['chuva_final', 'vazao', 'areakm']
# pasta_saida = './mapas_geoespaciais'
# os.makedirs(pasta_saida, exist_ok=True)

# # === LEITURA DO CSV ===
# df = pd.read_csv(arquivo)

# # Padronizar nomes
# df['municipio'] = df['municipio'].apply(lambda x: unidecode(str(x).strip().lower()))
# df['uf'] = df['uf'].str.upper()

# # === CARREGAR GEOMETRIAS ===
# gdf = read_municipality(year=2020, simplified=True)
# gdf = gdf[gdf['abbrev_state'].isin(['AC', 'AM', 'AP', 'MA', 'MT', 'PA', 'RO', 'RR', 'TO'])]

# # Padronizar nomes no GeoDataFrame
# gdf['nome_municipio'] = gdf['name_muni'].apply(lambda x: unidecode(x.strip().lower()))
# gdf['uf'] = gdf['abbrev_state']

# # === FAZER O MERGE ===
# gdf_merged = gdf.merge(df, left_on=['nome_municipio', 'uf'], right_on=['municipio', 'uf'])

# # === GERAR MAPAS PARA CADA VARIÁVEL ===
# for var in variaveis:
#     if var in gdf_merged.columns:
#         fig, ax = plt.subplots(figsize=(10, 8))

#         # Escalas e cores específicas por variável
#         if var == 'chuva_final':
#             vmin = 0
#             vmax = gdf_merged['chuva_final'].quantile(0.95)  # foco nos valores mais comuns
#             cmap = 'coolwarm'
#         elif var == 'vazao':
#             vmin = 0
#             vmax = gdf_merged['vazao'].quantile(0.95)  # foco nos valores mais comuns
#             cmap='seismic'
#         elif var == 'areakm':
#             vmin = 0
#             vmax = gdf_merged['areakm'].quantile(0.95)  # foco nos valores mais comuns
#             cmap = 'Greens'
#         else:
#             vmin = gdf_merged[var].min()
#             vmax = gdf_merged[var].max()
#             cmap = 'YlOrRd'

#         gdf_merged.plot(column=var,
#                         cmap=cmap,
#                         linewidth=0.5,
#                         edgecolor='black',
#                         legend=True,
#                         ax=ax,
#                         vmin=vmin,
#                         vmax=vmax)

#         plt.title(f'Distribuição Geoespacial de {var}', fontsize=14)
#         plt.axis('off')
#         plt.tight_layout()

#         nome_img = f'{pasta_saida}/mapa_{var}.png'
#         plt.savefig(nome_img)
#         plt.close()
#         print(f'🗺️ Mapa salvo: {nome_img}')
