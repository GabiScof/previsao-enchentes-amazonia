import pandas as pd
import matplotlib.pyplot as plt
import os

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
