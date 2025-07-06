import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

# Caminho base dos dados
BASE_DIR = Path("/mnt/c/Users/WHS/Documents/prev_prob_fogo/data/202411/CPTEC/")

# Dicionário de cores por categoria normalizada
'''
ALERTA_CORES = {
    "alert": "#FFD580",             # laranja claro
    "attention": "#FFFFB3",         # amarelo claro
    "high alert": "#FF9999",        # vermelho claro
    "low probability": "#ADD8E6",   # azul claro
    "observation": "#90EE90",       # verde claro
}
'''

ALERTA_CORES = {
    "alert": "#ffaa01",             # vermelho claro
    "attention": "#ffff00",         # vermelho médio
    "high alert": "#e60000",        # vermelho vivo
    "observation": "#89cd67",   # vermelho rosado
    "low probability": "#01c4ff",       # vermelho muito claro
}

COR_DEFAULT = "#CCCCCC"  # cinza para categorias desconhecidas

def plotar_estado_ms(filename: str, column: str = "alerta", title: str = "Mapa de Alerta - MS"):
    filepath = BASE_DIR / filename

    try:
        gdf = gpd.read_file(filepath)
    except Exception as e:
        print(f"❌ Erro ao carregar shapefile: {e}")
        return

    # Verificações
    if "SIGLA_UF" not in gdf.columns or column not in gdf.columns:
        print("❌ Colunas esperadas não encontradas.")
        print("Colunas disponíveis:", gdf.columns.tolist())
        return

    # Filtra MS
    gdf_ms = gdf[gdf["SIGLA_UF"] == "MS"].copy()

    if gdf_ms.empty:
        print("⚠️ Nenhum dado encontrado para SIGLA_UF = 'MS'")
        return

    # Normaliza os valores da coluna de alerta
    gdf_ms["alerta_normalizado"] = gdf_ms[column].astype(str).str.strip().str.lower()

    # Aplica as cores
    gdf_ms["cor"] = gdf_ms["alerta_normalizado"].map(ALERTA_CORES).fillna(COR_DEFAULT)

    # Plotagem
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf_ms.plot(ax=ax, color=gdf_ms["cor"], edgecolor="black", linewidth=0.5)
    plt.title(title, fontsize=15)
    plt.axis("off")
    plt.tight_layout()

    # Legenda com categorias encontradas
    import matplotlib.patches as mpatches
    categorias = gdf_ms["alerta_normalizado"].unique()[::-1]  # inverte a ordem
    legend_patches = [
        mpatches.Patch(color=ALERTA_CORES.get(cat, COR_DEFAULT), label=cat)
        for cat in categorias
    ]
    plt.legend(handles=legend_patches, title="Alerta", loc="lower left")

    # Salva imagem
    output_path = BASE_DIR / "mapa_MS_alerta_personalizado.png"
    plt.savefig(output_path, dpi=300)
    print(f"✅ Mapa salvo em: {output_path}")

    plt.show()

if __name__ == "__main__":
    plotar_estado_ms("NDJ_Cptec_CD_MUN_tabela_completa.shp")
