
import geopandas as gpd
from pathlib import Path

def listar_colunas_shapefile(nome_arquivo: str):
    """
    Abre um shapefile e imprime as colunas disponíveis.

    Args:
        nome_arquivo (str): Nome do arquivo .shp (ex: 'municipios.shp')
    """
    # Caminho absoluto ou relativo à pasta 'data'
    base_path = Path("/mnt/c/Users/WHS/Documents/prev_prob_fogo/data/202411/CPTEC/")
    caminho = base_path / nome_arquivo

    try:
        gdf = gpd.read_file(caminho)
        print(f"\n✅ Colunas do shapefile '{nome_arquivo}':\n")
        print(gdf.columns)
        print("\n🔍 Primeiras linhas dos dados:")
        print(gdf.head())
    except Exception as e:
        print(f"\n❌ Erro ao carregar o shapefile: {e}")

if __name__ == "__main__":
    listar_colunas_shapefile("NDJ_Cptec_CD_MUN_tabela_completa.shp")