import pandas as pd
import plotly.express as px
import os

df_xgb = pd.read_excel("data/plano-de-experimentacao/plano_de_experimentacao_final_2.xlsx", sheet_name="XGBoost Regressor")
df_rf = pd.read_excel("data/plano-de-experimentacao/plano_de_experimentacao_final_2.xlsx", sheet_name="Random Forest Regressor")

def identificar_preprocessamento(row):
    if row.get("Standard") == "X":
        return "StandardScaler"
    elif row.get("MinMax") == "X":
        return "MinMaxScaler"
    elif row.get("Robust") == "X":
        return "RobustScaler"
    else:
        return "Outro"

def identificar_outliers(row):
    return "Com Remoção" if row.get("Remoção de Outliers") == "X" or row.get("Remoção de Outliers.1") == "X" else "Sem Remoção"

def identificar_selecao(row):
    if row.get("RFE") == "X":
        return "RFE"
    elif row.get("SelectKBest") == "X":
        return "SelectKBest"
    else:
        return "Sem Seleção"

for df, nome in [(df_xgb, "XGBoost"), (df_rf, "Random Forest")]:
    df["Modelo"] = nome
    df["Pré-processamento"] = df.apply(identificar_preprocessamento, axis=1)
    df["Outliers"] = df.apply(identificar_outliers, axis=1)
    df["Seleção de Atributos"] = df.apply(identificar_selecao, axis=1)

df_comparativo = pd.concat([df_xgb, df_rf], ignore_index=True)

output_path = "data/plano-de-experimentacao/analise-graficos"
os.makedirs(output_path, exist_ok=True)

def gerar_grafico(coluna, titulo, nome_arquivo):
    resumo = df_comparativo.groupby(["Modelo", coluna])["R²"].agg(["mean", "std"]).reset_index()
    fig = px.bar(
        resumo,
        x=coluna,
        y="mean",
        color="Modelo",
        error_y="std",
        barmode="group",
        labels={"mean": "R² Médio"},
        title=titulo
    )
    fig.update_layout(
        title_font=dict(size=20),
        yaxis_title="R² Médio",
        xaxis_title=coluna,
        legend_title_text="Algoritmo"
    )
    caminho = os.path.join(output_path, nome_arquivo)
    fig.write_image(caminho, format='png', scale=3, width=1000, height=600)
    print(f"Gráfico salvo em: {caminho}")

gerar_grafico("Pré-processamento", "Desempenho por Tipo de Normalização", "grafico_r2_por_normalizacao.png")
gerar_grafico("Outliers", "Desempenho com e sem Remoção de Outliers", "grafico_r2_por_outliers.png")
gerar_grafico("Seleção de Atributos", "Desempenho por Método de Seleção de Atributos", "grafico_r2_por_selecao.png")
