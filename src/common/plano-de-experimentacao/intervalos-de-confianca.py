import pandas as pd
import numpy as np
import scipy.stats as st

file_path = 'data/plano-de-experimentacao/plano_de_experimentacao_final_2.xlsx'

df_xgb = pd.read_excel(file_path, sheet_name='XGBoost Regressor')
df_rf = pd.read_excel(file_path, sheet_name='Random Forest Regressor')

def intervalo_confianca_r2(series, confianca=0.95):
    media = np.mean(series)
    desvio = np.std(series, ddof=1)
    n = len(series)
    z = st.norm.ppf(1 - (1 - confianca) / 2)  
    erro = z * desvio / np.sqrt(n)
    return media, media - erro, media + erro

r2_xgb = df_xgb["R²"].dropna()
r2_rf = df_rf["R²"].dropna()

ic_xgb = intervalo_confianca_r2(r2_xgb)
ic_rf = intervalo_confianca_r2(r2_rf)

resultado_ic = pd.DataFrame({
    "Modelo": ["XGBoost", "Random Forest"],
    "R² Médio": [ic_xgb[0], ic_rf[0]],
    "IC Inferior (95%)": [ic_xgb[1], ic_rf[1]],
    "IC Superior (95%)": [ic_xgb[2], ic_rf[2]]
})

print(resultado_ic)
