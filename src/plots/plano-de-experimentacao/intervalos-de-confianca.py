import pandas as pd
import numpy as np
import scipy.stats as st

file_path = 'data/plano-de-experimentacao/plano_de_experimentacao_final_2.xlsx'

df_xgb = pd.read_excel(file_path, sheet_name='XGBoost Regressor')
df_rf = pd.read_excel(file_path, sheet_name='Random Forest Regressor')

def intervalo_confianca(series, confianca=0.95):
    media = np.mean(series)
    desvio = np.std(series, ddof=1)
    n = len(series)
    z = st.norm.ppf(1 - (1 - confianca) / 2) 
    erro = z * desvio / np.sqrt(n)
    return media, media - erro, media + erro

ic_r2_xgb = intervalo_confianca(df_xgb["R²"].dropna())
ic_r2_rf = intervalo_confianca(df_rf["R²"].dropna())

ic_mae_xgb = intervalo_confianca(df_xgb["MAE"].dropna())
ic_mae_rf = intervalo_confianca(df_rf["MAE"].dropna())

ic_rmse_xgb = intervalo_confianca(df_xgb["MSE"].dropna())
ic_rmse_rf = intervalo_confianca(df_rf["MSE"].dropna())

resultado_ic_mae = pd.DataFrame({
    "Modelo": ["XGBoost", "Random Forest"],
    "MAE Médio": [ic_mae_xgb[0], ic_mae_rf[0]],
    "IC Inferior (95%)": [ic_mae_xgb[1], ic_mae_rf[1]],
    "IC Superior (95%)": [ic_mae_xgb[2], ic_mae_rf[2]]
})

resultado_ic_rmse = pd.DataFrame({
    "Modelo": ["XGBoost", "Random Forest"],
    "RMSE Médio": [ic_rmse_xgb[0], ic_rmse_rf[0]],
    "IC Inferior (95%)": [ic_rmse_xgb[1], ic_rmse_rf[1]],
    "IC Superior (95%)": [ic_rmse_xgb[2], ic_rmse_rf[2]]
})

resultado_ic_r2 = pd.DataFrame({
    "Modelo": ["XGBoost", "Random Forest"],
    "R² Médio": [ic_r2_xgb[0], ic_r2_rf[0]],
    "IC Inferior (95%)": [ic_r2_xgb[1], ic_r2_rf[1]],
    "IC Superior (95%)": [ic_r2_xgb[2], ic_r2_rf[2]]
})

print("\nIntervalos de Confiança para R²:")
print(resultado_ic_r2)

print("\nIntervalos de Confiança para MAE:")
print(resultado_ic_mae)

print("\nIntervalos de Confiança para MSE:")
print(resultado_ic_rmse)
