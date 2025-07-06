import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec # Keep this if you plan to reintroduce the table
from pathlib import Path

# Cores suaves em tons de vermelho
ALERTA_CORES = {
    "alert": "#ffaa01",           # laranja
    "attention": "#ffff00",        # amarelo
    "high alert": "#e60000",       # vermelho vivo
    "observation": "#89cd67",      # verde claro
    "low probability": "#01c4ff",  # azul claro
}

ALERTA_TRADUZIDO = {
    "high alert": "Alerta Alto",
    "alert": "Alerta",
    "attention": "Atenção",
    "low probability": "Baixa probabilidade",
    "observation": "Observação",
}

COR_DEFAULT = "#CCCCCC"  # Cor cinza para estados sem alerta ou fora da seleção

BASE_DIR = Path("/mnt/c/Users/WHS/Documents/prev_prob_fogo/data/202411/CPTEC/")

def plotar_estados(
    filename: str,
    ufs: list[str],
    column: str = "alerta",
    title: str = "Mapa de Alerta",
    ordem_legenda: list[str] = None
):
    filepath = BASE_DIR / filename

    try:
        # Load the complete shapefile, which should contain all Brazil states/municipalities
        gdf_completo = gpd.read_file(filepath)
    except Exception as e:
        print(f"❌ Erro ao carregar shapefile: {e}")
        return

    if "SIGLA_UF" not in gdf_completo.columns or column not in gdf_completo.columns:
        print("❌ Colunas esperadas não encontradas.")
        print("Colunas disponíveis:", gdf_completo.columns.tolist())
        return

    # Filter for the desired states
    gdf_estados_selecionados = gdf_completo[gdf_completo["SIGLA_UF"].isin(ufs)].copy()

    if gdf_estados_selecionados.empty:
        print(f"⚠️ Nenhum dado encontrado para os estados: {ufs}")
        return

    # Normalize the 'alerta' column for selected states
    gdf_estados_selecionados["alerta_normalizado"] = gdf_estados_selecionados[column].astype(str).str.strip().str.lower()
    gdf_estados_selecionados["cor"] = gdf_estados_selecionados["alerta_normalizado"].map(ALERTA_CORES).fillna(COR_DEFAULT)

    # --- Plotting Setup ---
    fig, ax = plt.subplots(figsize=(22, 19))

    # 1. Plot the *entire* Brazil outline (all municipalities from the loaded shapefile)
    # Give them a default gray color and a thin black border
    gdf_completo.plot(ax=ax, color="#E0E0E0", edgecolor="grey", linewidth=0.3)

    # 2. Plot the *selected* states on top with their specific colors
    # Ensure they have a slightly thicker border to stand out
    gdf_estados_selecionados.plot(ax=ax, color=gdf_estados_selecionados["cor"], edgecolor="black", linewidth=0.8)

    # 3. Plot the *dissolved borders* of the selected states with an even thicker line
    # This creates a strong outline for the group of selected states
    gdf_estados_selecionados_dissolved = gdf_estados_selecionados.dissolve(by="SIGLA_UF")
    gdf_estados_selecionados_dissolved.plot(ax=ax, facecolor='none', edgecolor="black", linewidth=1.0)

    ax.set_title(title, fontsize=16)
    ax.axis("off") # Turn off axes for a cleaner map

    # --- Legend ---
    if ordem_legenda:
        # Ensure only unique alert levels present in selected states are in the legend
        categorias_legenda = [c for c in ordem_legenda if c in gdf_estados_selecionados["alerta_normalizado"].unique()]
    else:
        categorias_legenda = sorted(gdf_estados_selecionados["alerta_normalizado"].unique())

    legend_patches = [
        mpatches.Patch(color=ALERTA_CORES.get(cat, COR_DEFAULT), label=ALERTA_TRADUZIDO.get(cat, cat))
        for cat in categorias_legenda
    ]
    ax.legend(handles=legend_patches, title="Nível de Alerta", loc="lower left", bbox_to_anchor=(0, -0.15)) # Adjust bbox_to_anchor if needed

    # --- Saving and Displaying ---
    estados_nome = "_".join(ufs)
    output_path = BASE_DIR / f"mapa_{estados_nome}_alerta_com_contorno_brasil.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight') # Use bbox_inches='tight' for better saving
    print(f"✅ Mapa salvo em: {output_path}")

    plt.show()

if __name__ == "__main__":
    ufs_desejadas = ["MS", "MT", "GO", "DF", "RS", "AL","AC"]
    ordem_personalizada = ["high alert", "alert", "attention", "observation", "low probability"]
    
    plotar_estados(
        filename="NDJ_Cptec_CD_MUN_tabela_completa.shp",
        ufs=ufs_desejadas,
        title="Mapa de Alerta - MS, MT, GO, DF, RS e AL com Contorno do Brasil",
        ordem_legenda=ordem_personalizada
    )