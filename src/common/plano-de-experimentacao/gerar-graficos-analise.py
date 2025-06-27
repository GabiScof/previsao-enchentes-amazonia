import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px

# XGBoost

df = pd.read_excel('data/plano-de-experimentacao/plano_de_experimentacao_final_2.xlsx', sheet_name='XGBoost Regressor')

def identificar_cv(row):
    if row.get("KFold k=3") == "X":
        return "KFold k=3"
    elif row.get("KFold k=10") == "X":
        return "KFold k=10"
    elif row.get("RepeatedKFold 5x2") == "X":
        return "RepeatedKFold 5x2"
    else:
        return "Outro"

df["Validação Cruzada"] = df.apply(identificar_cv, axis=1)

resumo = df.groupby("Validação Cruzada")["R²"].agg(["mean", "std"]).reset_index()

plt.figure(figsize=(10, 6))
plt.bar(resumo["Validação Cruzada"], resumo["mean"], yerr=resumo["std"], capsize=8)
plt.ylabel("R² Médio")
plt.title("Desempenho Médio por Estratégia de Validação Cruzada (com Desvio Padrão)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

output_path = 'data/plano-de-experimentacao/analise-graficos'
os.makedirs(output_path, exist_ok=True)

saida = os.path.join(output_path, 'grafico_validacao_cruzada_xgb.png')
print("Salvando em:", os.path.abspath(saida)) 

plt.savefig(saida, dpi=300, bbox_inches='tight') 

plt.close() 


# Random Forest

df = pd.read_excel('data/plano-de-experimentacao/plano_de_experimentacao_final_2.xlsx', sheet_name='Random Forest Regressor')

def identificar_cv(row):
    if row.get("KFold k=3") == "X":
        return "KFold k=3"
    elif row.get("KFold k=10") == "X":
        return "KFold k=10"
    elif row.get("RepeatedKFold 5x2") == "X":
        return "RepeatedKFold 5x2"
    else:
        return "Outro"

df["Validação Cruzada"] = df.apply(identificar_cv, axis=1)

resumo = df.groupby("Validação Cruzada")["R²"].agg(["mean", "std"]).reset_index()

plt.figure(figsize=(10, 6))
plt.bar(resumo["Validação Cruzada"], resumo["mean"], yerr=resumo["std"], capsize=8)
plt.ylabel("R² Médio")
plt.title("Desempenho Médio por Estratégia de Validação Cruzada (com Desvio Padrão)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

output_path = 'data/plano-de-experimentacao/analise-graficos'
os.makedirs(output_path, exist_ok=True)

saida = os.path.join(output_path, 'grafico_validacao_cruzada_rf.png')
print("Salvando em:", os.path.abspath(saida)) 

plt.savefig(saida, dpi=300, bbox_inches='tight') 

plt.close() 


# Comparação dos dois

df_xgb = pd.read_excel('data/plano-de-experimentacao/plano_de_experimentacao_final_2.xlsx', sheet_name='XGBoost Regressor')
df_xgb["Validação Cruzada"] = df_xgb.apply(identificar_cv, axis=1)
resumo_xgb = df_xgb.groupby("Validação Cruzada")["R²"].agg(["mean", "std"]).reset_index()
resumo_xgb["Algoritmo"] = "XGBoost"

df_rf = pd.read_excel('data/plano-de-experimentacao/plano_de_experimentacao_final_2.xlsx', sheet_name='Random Forest Regressor')
df_rf["Validação Cruzada"] = df_rf.apply(identificar_cv, axis=1)
resumo_rf = df_rf.groupby("Validação Cruzada")["R²"].agg(["mean", "std"]).reset_index()
resumo_rf["Algoritmo"] = "Random Forest"

resumo_total = pd.concat([resumo_xgb, resumo_rf], ignore_index=True)

fig = px.bar(
    resumo_total,
    x="Validação Cruzada",
    y="mean",
    color="Algoritmo",
    error_y="std",
    barmode="group",
    labels={"mean": "R² Médio", "Validação Cruzada": "Estratégia de Validação Cruzada"},
    title="Desempenho Médio dos Algoritmos Por Estratégia De Validação"
)

fig.update_layout(
    title_font=dict(size=20),
    xaxis_tickangle=-25,
    yaxis=dict(title="R² Médio"),
    legend_title_text="Algoritmo"
)

output_path = 'data/plano-de-experimentacao/analise-graficos'
os.makedirs(output_path, exist_ok=True)

saida = os.path.join(output_path, 'grafico_validacao_cruzada_comparacao.png')
print("Salvando em:", os.path.abspath(saida))

fig.write_image(saida, format='png', scale=3, width=1000, height=600)