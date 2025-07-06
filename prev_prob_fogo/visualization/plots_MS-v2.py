import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# Paleta de tons de vermelho suaves
ALERTA_CORES = {
    "alert": "#ffaa01",             # vermelho claro
    "attention": "#ffff00",         # vermelho médio
    "high alert": "#e60000",        # vermelho vivo
    "observation": "#89cd67",   # vermelho rosado
    "low probability": "#01c4ff",       # vermelho muito claro
}

COR_DEFAULT = "#CCCCCC"  # cinza para valores não mapeados

BASE_DIR = Path("/mnt/c/Users/WHS/Documents/prev_prob_fogo/data/202411/CPTEC/")


def plotar_estado_ms(
    filename: str,
    column: str = "alerta",
    title: str = "Mapa de Alerta - MS",
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

    gdf_ms = gdf[gdf["SIGLA_UF"] == "MS"].copy()

    if gdf_ms.empty:
        print("⚠️ Nenhum dado encontrado para SIGLA_UF = 'MS'")
        return

    # Normaliza a coluna de alerta
    gdf_ms["alerta_normalizado"] = gdf_ms[column].astype(str).str.strip().str.lower()

    # Aplica cores
    gdf_ms["cor"] = gdf_ms["alerta_normalizado"].map(ALERTA_CORES).fillna(COR_DEFAULT)

    # Plotagem
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf_ms.plot(ax=ax, color=gdf_ms["cor"], edgecolor="black", linewidth=0.5)
    plt.title(title, fontsize=15)
    plt.axis("off")
    plt.tight_layout()

    # Geração da legenda personalizada
    if ordem_legenda:
        categorias_legenda = [c for c in ordem_legenda if c in gdf_ms["alerta_normalizado"].unique()]
    else:
        categorias_legenda = sorted(gdf_ms["alerta_normalizado"].unique())

    legend_patches = [
        mpatches.Patch(color=ALERTA_CORES.get(cat, COR_DEFAULT), label=cat)
        for cat in categorias_legenda
    ]
    plt.legend(handles=legend_patches, title="Alerta", loc="lower left")

    # Salvar imagem
    output_path = BASE_DIR / "mapa_MS_alerta_personalizado.png"
    plt.savefig(output_path, dpi=300)
    print(f"✅ Mapa salvo em: {output_path}")

    plt.show()


if __name__ == "__main__":
    ordem_personalizada = ["high alert", "alert", "attention", "observation","low probability"]
    plotar_estado_ms(
        filename="NDJ_Cptec_CD_MUN_tabela_completa.shp",
        ordem_legenda=ordem_personalizada
    )
