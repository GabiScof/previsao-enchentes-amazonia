import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df_xgb = pd.read_excel('data/plano-de-experimentacao/plano_de_experimentacao_final_2.xlsx',
                       sheet_name='XGBoost Regressor')
df_rf = pd.read_excel('data/plano-de-experimentacao/plano_de_experimentacao_final_2.xlsx',
                      sheet_name='Random Forest Regressor')

df_xgb['Algoritmo'] = 'XGBoost'
df_rf['Algoritmo'] = 'Random Forest'

df = pd.concat([df_xgb, df_rf], ignore_index=True)

df = df.rename(columns={'R²': 'R2'})

df['RMSE'] = df['MSE']**0.5

desempenho_medio = df.groupby('Algoritmo')[['R2', 'MAE', 'MSE', 'RMSE']].mean().reset_index()

fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Métricas Médias por Algoritmo', fontsize=14)

metricas = ['R2', 'MAE', 'MSE', 'RMSE']
titulos = ['R² Médio', 'MAE Médio', 'MSE Médio', 'RMSE Médio']
cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd']

for i, (ax, metrica, titulo, cor) in enumerate(zip(axs.ravel(), metricas, titulos, cores)):
    sns.barplot(data=desempenho_medio, x='Algoritmo', y=metrica, ax=ax, color=cor)
    ax.set_title(titulo)
    ax.set_ylabel('Valor Médio')
    ax.set_xlabel('')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()


arquivo = 'data/plano-de-experimentacao/plano_de_experimentacao_final_2.xlsx'
df_xgb = pd.read_excel(arquivo, sheet_name='XGBoost Regressor')
df_rf = pd.read_excel(arquivo, sheet_name='Random Forest Regressor')

df_xgb = df_xgb.rename(columns={'R²': 'R2'})
df_rf = df_rf.rename(columns={'R²': 'R2'})

df_xgb['RMSE'] = np.sqrt(df_xgb['MSE'])
df_rf['RMSE'] = np.sqrt(df_rf['MSE'])

medias_xgb = df_xgb[['MAE', 'MSE', 'RMSE', 'R2']].mean()
medias_rf = df_rf[['MAE', 'MSE', 'RMSE', 'R2']].mean()

tabela = pd.DataFrame({
    'Métrica': [
        'MAE (Mean Absolute Error)',
        'MSE (Mean Squared Error)',
        'RMSE (Root Mean Squared Error)',
        'R² (Coeficiente de Determinação)'
    ],
    'XGBoost': [
        round(medias_xgb['MAE'], 2),
        round(medias_xgb['MSE'], 2),
        round(medias_xgb['RMSE'], 2),
        round(medias_xgb['R2'], 4)
    ],
    'Random Forest': [
        round(medias_rf['MAE'], 2),
        round(medias_rf['MSE'], 2),
        round(medias_rf['RMSE'], 2),
        round(medias_rf['R2'], 4)
    ]
})

print(tabela.to_string(index=False))
