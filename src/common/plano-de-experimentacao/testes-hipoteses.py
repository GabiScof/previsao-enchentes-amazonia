import pandas as pd
import numpy as np
import scipy.stats as stats

file_path = 'data/plano-de-experimentacao/plano_de_experimentacao_final_2.xlsx'
df_xgb = pd.read_excel(file_path, sheet_name='XGBoost Regressor')
df_rf = pd.read_excel(file_path, sheet_name='Random Forest Regressor')

mse_xgb = df_xgb["MSE"].dropna()
mse_rf = df_rf["MSE"].dropna()

mae_xgb = df_xgb["MAE"].dropna()
mae_rf = df_rf["MAE"].dropna()

r2_xgb = df_xgb["R²"].dropna()
r2_rf = df_rf["R²"].dropna()

teste_mse = stats.ttest_ind(mse_xgb, mse_rf, equal_var=False)
teste_mae = stats.ttest_ind(mae_xgb, mae_rf, equal_var=False)
teste_r2  = stats.ttest_ind(r2_xgb, r2_rf, equal_var=False)

resultados_hipotese = pd.DataFrame({
    "Métrica": ["MSE", "MAE", "R²"],
    "Estatística t": [teste_mse.statistic, teste_mae.statistic, teste_r2.statistic],
    "p-valor": [teste_mse.pvalue, teste_mae.pvalue, teste_r2.pvalue]
})

print("Resultados dos Testes de Hipóteses:")
print(resultados_hipotese)