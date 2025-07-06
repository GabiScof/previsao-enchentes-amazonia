import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr

df = pd.read_csv('../../data/pre-processados/dados-sem-clima-finais.csv')

# Primeiro, vamos garantir que ano e mês são inteiros:
df['ano'] = df['ano'].astype(int)
df['mes'] = df['mes'].astype(int)

# (1) Chuva, Vazão e Desmatamento - ao longo dos anos (todos os municípios)
df_grouped = df.groupby('ano').agg({
    'chuva_final': 'mean',
    'vazao': 'mean',
    'areakm': 'mean'
}).reset_index()

# Normalizar entre 0 e 1
df_grouped_norm = df_grouped.copy()
for col in ['chuva_final', 'vazao', 'areakm']:
    df_grouped_norm[col] = (df_grouped[col] - df_grouped[col].min()) / (df_grouped[col].max() - df_grouped[col].min())

# Plot
plt.figure(figsize=(12,6))
plt.plot(df_grouped_norm['ano'], df_grouped_norm['chuva_final'], label='Chuva (normalizado)', marker='o')
plt.plot(df_grouped_norm['ano'], df_grouped_norm['vazao'], label='Vazão (normalizado)', marker='s')
plt.plot(df_grouped_norm['ano'], df_grouped_norm['areakm'], label='Área (normalizado)', marker='^')
plt.title('Média Anual Normalizada')
plt.xlabel('Ano')
plt.ylabel('Valor Normalizado (0-1)')
plt.legend()
plt.grid(True)
plt.show()

# ----------------------------------------------------

# (3) Correlação entre Variáveis
plt.figure(figsize=(8,6))
plt.scatter(df['chuva_final'], df['vazao'], alpha=0.6)
plt.title('Correlação entre Chuva e Vazão')
plt.xlabel('Chuva (mm)')
plt.ylabel('Vazão (m³/s)')
plt.grid(True)
plt.savefig('../../data/analise-dados/correlacao_chuva_vazao.png', dpi=300, bbox_inches='tight')
plt.show()


# ----------------------------------------------------

# (4) Chuva média mensal ao longo do ano (todos os municípios juntos)
chuva_mensal = df.groupby('mes')['chuva_final'].mean()

plt.figure(figsize=(10,5))
plt.bar(chuva_mensal.index, chuva_mensal.values)
plt.title('Chuva Média por Mês')
plt.xlabel('Mês')
plt.ylabel('Chuva Média (mm)')
plt.xticks(range(1,13))
plt.grid(axis='y')
plt.savefig('../../data/analise-dados/chuva-media-mes.png', dpi=300, bbox_inches='tight')
plt.show()

# (4) Chuva média mensal ao longo do ano (todos os municípios juntos)
vazao_mensal = df.groupby('mes')['vazao'].mean()

plt.figure(figsize=(10,5))
plt.bar(vazao_mensal.index, vazao_mensal.values)
plt.title('Vazão Média por Mês')
plt.xlabel('Mês')
plt.ylabel('Vazão Média (mm)')
plt.xticks(range(1,13))
plt.grid(axis='y')
plt.savefig('../../data/analise-dados/vazao-media-mes.png', dpi=300, bbox_inches='tight')
plt.show()

# ----------------------------------------------------

# Criar lag de chuva (chuva de mês anterior)
df = df.sort_values(['municipio', 'ano', 'mes']).copy()
df['chuva_lag1'] = df.groupby('municipio')['chuva_final'].shift(1)

# Tratar outliers de vazão
# Usar IQR para detectar outliers
Q1 = df['vazao'].quantile(0.25)
Q3 = df['vazao'].quantile(0.75)
IQR = Q3 - Q1
filtro = (df['vazao'] >= (Q1 - 1.5 * IQR)) & (df['vazao'] <= (Q3 + 1.5 * IQR))
df_limpo = df[filtro].copy()

# Separar por município
# Exemplo: pegar um município específico para analisar
municipios_exemplo = df_limpo['municipio'].value_counts().index[:5]  # 5 municípios com mais dados

for municipio in municipios_exemplo:
    df_mun = df_limpo[df_limpo['municipio'] == municipio]

    plt.scatter(df_mun['chuva_lag1'], df_mun['vazao'], alpha=0.5)
    plt.title(f'Chuva (lag 1 mês) vs Vazão - {municipio.title()}')
    plt.xlabel('Chuva do Mês Anterior (mm)')
    plt.ylabel('Vazão (m³/s)')
    plt.grid(True)
    plt.savefig(f'../../data/analise-dados/correlacao-vazao-chuva-{municipio}.png', dpi=300, bbox_inches='tight')
    plt.show()

#Calcular correlação Spearman (em todos os dados tratados)
# Ignorar valores NaN que surgiram no lag
df_corr = df_limpo.dropna(subset=['chuva_lag1', 'vazao'])

corr_pearson = df_corr['chuva_lag1'].corr(df_corr['vazao'], method='pearson')
corr_spearman, _ = spearmanr(df_corr['chuva_lag1'], df_corr['vazao'])

print(f"Correlação de Pearson (linear): {corr_pearson:.4f}")
print(f"Correlação de Spearman (tendência): {corr_spearman:.4f}")

# 🔥 Matriz de Correlação Spearman geral
corr_matrix = df_corr[['chuva_lag1', 'vazao']].corr(method='spearman')
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Matriz de Correlação - Método Spearman')
plt.savefig(f'../../data/analise-dados/matriz-correlacao.png', dpi=300, bbox_inches='tight')
plt.show()


# -----------------------------------------------------------

# Exemplo se quiser fazer com chuva lag de 1 mês:
municipios = df['municipio'].unique()

# Lista para guardar resultados
resultados = []

# Loop em cada município
for municipio in municipios:
    df_mun = df[df['municipio'] == municipio].dropna(subset=['chuva_lag1', 'vazao'])

    if len(df_mun) > 10:  # Só calcular se tiver pelo menos 10 dados
        corr_spearman, _ = spearmanr(df_mun['chuva_lag1'], df_mun['vazao'])
        resultados.append({'municipio': municipio, 'correlacao_spearman': corr_spearman})

# Transformar em DataFrame
df_corr_municipios = pd.DataFrame(resultados)

# Ordenar pelo valor da correlação
df_corr_municipios = df_corr_municipios.sort_values(by='correlacao_spearman', ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(df_corr_municipios['municipio'].head(10), df_corr_municipios['correlacao_spearman'].head(10))
plt.xlabel('Correlação de Spearman')
plt.title('Top 10 Municípios - Correlação Chuva (Lag 1) vs Vazão')
plt.gca().invert_yaxis()
plt.grid(True)
plt.savefig(f'../../data/analise-dados/correlacao-por-municipios.png', dpi=300, bbox_inches='tight')
plt.show()

# Criar o DataFrame
df_corr_municipios = pd.DataFrame(resultados)
df_corr_municipios = df_corr_municipios.sort_values(by='correlacao_spearman', ascending=False).reset_index(drop=True)
df_corr_municipios.columns = ['Município', 'Correlação de Spearman']
df_corr_municipios.to_csv('../../data/analise-dados/correlacao_municipios.csv', index=False)
