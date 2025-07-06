import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path("/mnt/c/Users/WHS/Documents/prev_prob_fogo/data/202411/CPTEC/")
ufs_desejadas = ["MS", "MT", "GO", "DF"]

# Carregar CSV
df = pd.read_csv(BASE_DIR / f"tabela_resumo_{'_'.join(ufs_desejadas)}.csv", sep=";")

# Ordem dos níveis de alerta (em português)
ordem_alerta = ["Alerta Alto", "Alerta", "Atenção", "Baixa probabilidade", "Observação"]
df["ordem"] = df["Nível de Alerta"].apply(lambda x: ordem_alerta.index(x) if x in ordem_alerta else 99)
df = df.sort_values("ordem")

# Conversões
df["Número de municípios"] = pd.to_numeric(df["Número de municípios"], errors="coerce")
df["Área_km2_float"] = df["Área (km²)"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)

# Dicionário de cores mapeando os nomes originais
cores_alerta = {
    "Alerta": "#ffaa01",
    "Atenção": "#ffff00",
    "Alerta Alto": "#e60000",
    "Observação": "#89cd67",
    "Baixa probabilidade": "#01c4ff"
}

# Criar gráfico lado a lado
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Cores por alerta (lista na ordem do DataFrame)
cores = df["Nível de Alerta"].map(cores_alerta)

# --- Gráfico 1: Número de municípios ---
bars1 = ax1.barh(df["Nível de Alerta"], df["Número de municípios"], color=cores)

for bar in bars1:
    width = bar.get_width()
    texto = f"{int(width)}"
    ax1.text(width - 1, bar.get_y() + bar.get_height()/2, texto, va='center', ha='right', color="white", fontsize=9, fontweight="bold")

ax1.set_title("Número de Municípios")
ax1.set_xlabel("Municípios")
ax1.invert_yaxis()

# --- Gráfico 2: Área total ---
bars2 = ax2.barh(df["Nível de Alerta"], df["Área_km2_float"], color=cores)

for i, bar in enumerate(bars2):
    width = bar.get_width()
    area_label = df.iloc[i]["Área (km²)"]
    ax2.text(width - (width * 0.01), bar.get_y() + bar.get_height()/2, area_label, va='center', ha='right', color="white", fontsize=9, fontweight="bold")

ax2.set_title("Área Total (km²)")
ax2.set_xlabel("Área (km²)")

# Layout final
plt.suptitle("Resumo por Nível de Alerta", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()