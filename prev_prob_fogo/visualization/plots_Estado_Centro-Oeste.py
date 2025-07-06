import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# Cores suaves em tons de vermelho
ALERTA_CORES = {
    "alert": "#ffaa01",             # vermelho claro
    "attention": "#ffff00",         # vermelho médio
    "high alert": "#e60000",        # vermelho vivo
    "observation": "#89cd67",   # vermelho rosado
    "low probability": "#01c4ff",       # vermelho muito claro
}

ALERTA_TRADUZIDO = {
    "high alert": "Alerta Alto",
    "alert": "Alerta",
    "attention": "Atenção",
    "low probability": "Baixa probabilidade",
    "observation": "Observação",
}

COR_DEFAULT = "#CCCCCC"  # Cor cinza para valores não reconhecidos

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
        gdf = gpd.read_file(filepath)
    except Exception as e:
        print(f"❌ Erro ao carregar shapefile: {e}")
        return

    if "SIGLA_UF" not in gdf.columns or column not in gdf.columns:
        print("❌ Colunas esperadas não encontradas.")
        print("Colunas disponíveis:", gdf.columns.tolist())
        return

    # Filtrar pelos estados desejados
    gdf_estados = gdf[gdf["SIGLA_UF"].isin(ufs)].copy()

    if gdf_estados.empty:
        print(f"⚠️ Nenhum dado encontrado para os estados: {ufs}")
        return

    # Normalizar a coluna de alerta
    gdf_estados["alerta_normalizado"] = gdf_estados[column].astype(str).str.strip().str.lower()

    # Atribuir cores
    gdf_estados["cor"] = gdf_estados["alerta_normalizado"].map(ALERTA_CORES).fillna(COR_DEFAULT)

    # --- Plotting Setup ---
    fig, ax = plt.subplots(figsize=(12, 12))
    gdf_estados.plot(ax=ax, color=gdf_estados["cor"], edgecolor="black", linewidth=0.5)
    gdf_estados_dissolved = gdf_estados.dissolve(by="SIGLA_UF")
    # Depois, plota esses polígonos com uma borda mais grossa
    gdf_estados_dissolved.plot(ax=ax, facecolor='none', edgecolor="black", linewidth=2.0) # Linha mais grossa aqui

    ax.set_title(title, fontsize=16)
    ax.axis("off")

    # Legenda
    if ordem_legenda:
        categorias_legenda = [c for c in ordem_legenda if c in gdf_estados["alerta_normalizado"].unique()]
    else:
        categorias_legenda = sorted(gdf_estados["alerta_normalizado"].unique())

    legend_patches = [
        mpatches.Patch(color=ALERTA_CORES.get(cat, COR_DEFAULT), label=ALERTA_TRADUZIDO.get(cat, cat))
        for cat in categorias_legenda
    ]
    ax.legend(handles=legend_patches, title="Nível de Alerta", loc="lower left")

    # Salvar imagem
    estados_nome = "_".join(ufs)
    output_path = BASE_DIR / f"mapa_{estados_nome}_alerta.png"
    plt.savefig(output_path, dpi=300)
    print(f"✅ Mapa salvo em: {output_path}")

    plt.show()

if __name__ == "__main__":
    ufs_desejadas = ["MS", "MT", "GO", "DF", "RS","AL"]
    ordem_personalizada = ["high alert", "alert", "attention", "observation", "low probability"]
    plotar_estados(
        filename="NDJ_Cptec_CD_MUN_tabela_completa.shp",
        ufs=ufs_desejadas,
        title="Mapa de Alerta - MS, MT, GO e DF",
        ordem_legenda=ordem_personalizada
    )
