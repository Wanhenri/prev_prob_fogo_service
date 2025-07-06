import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

# Caminho base onde está o shapefile
BASE_DIR = Path("/mnt/c/Users/WHS/Documents/prev_prob_fogo/data/202411/CPTEC/")

def plot_shapefile(filename: str, column: str = None, cmap: str = "viridis", title: str = ""):
    """
    Plota um shapefile com base em uma coluna de dados (opcional).

    Args:
        filename (str): Nome do arquivo .shp (ex: 'NDJ_Cptec_CD_MUN_tabela_completa.shp')
        column (str): Nome da coluna para colorir os polígonos (opcional)
        cmap (str): Colormap a ser usado
        title (str): Título do gráfico
    """
    filepath = BASE_DIR / filename

    try:
        gdf = gpd.read_file(filepath)
    except Exception as e:
        print(f"❌ Erro ao ler o shapefile '{filename}': {e}")
        return

    if column and column not in gdf.columns:
        print(f"\n❌ A coluna '{column}' não foi encontrada no arquivo '{filename}'.")
        print("📋 Colunas disponíveis:")
        for col in gdf.columns:
            print(f" - {col}")
        return

    fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(ax=ax, column=column, cmap=cmap, legend=bool(column))
    plt.title(title or f"Mapa: {filename}", fontsize=15)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

plot_shapefile(
    "NDJ_Cptec_CD_MUN_tabela_completa.shp",
    column="alerta",
    title="Mapa de Alerta de Incêndio"
)