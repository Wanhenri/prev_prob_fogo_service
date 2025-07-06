import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from pathlib import Path

# Cores suaves em tons de vermelho
ALERTA_CORES = {
    "alert": "#ffaa01",
    "attention": "#ffff00",
    "high alert": "#e60000",
    "observation": "#89cd67",
    "low probability": "#01c4ff",
}

# Tradução dos rótulos para português
ALERTA_TRADUZIDO = {
    "high alert": "Alerta Alto",
    "alert": "Alerta",
    "attention": "Atenção",
    "low probability": "Baixa probabilidade",
    "observation": "Observação",
}

COR_DEFAULT = "#CCCCCC"

BASE_DIR = Path("/mnt/c/Users/WHS/Documents/prev_prob_fogo/data/202411/CPTEC/")

def gerar_tabela_resumo(gdf_estados, coluna_alerta="alerta_normalizado", nome_arquivo="NDJ_Cptec_CD_MUN_tabela_completa.csv"):
    # Verificar se tem coluna de área, senão calcular área geográfica em km²
    if "area_km2" in gdf_estados.columns:
        gdf_estados["area_km2"] = gdf_estados["area_km2"].astype(float)
    else:
        # Calcular área do polígono em graus, transformar para km² com EPSG: 5880 ou proj. métrica (exemplo UTM)
        # Para isso precisamos reprojetar para sistema métrico:
        gdf_metrico = gdf_estados.to_crs(epsg=5880)  # Sistema métrico local (você pode ajustar se preferir UTM da região)
        gdf_estados["area_km2"] = gdf_metrico.geometry.area / 1e6  # m² para km²
    
    # Agrupar por nível de alerta e calcular número de municípios e soma da área
    resumo = (
        gdf_estados.groupby(coluna_alerta)
        .agg(
            numero_municipios=("SIGLA_UF", "count"),
            area_km2=("area_km2", "sum")
        )
        .reset_index()
    )
    
    # Dicionário para tradução dos níveis de alerta
    traducao_alerta = {
        "high alert": "Alerta Alto",
        "alert": "Alerta",
        "attention": "Atenção",
        "low probability": "Baixa probabilidade",
        "observation": "Observação"
    }
    
    # Traduzir nomes do nível de alerta
    resumo[coluna_alerta] = resumo[coluna_alerta].map(traducao_alerta).fillna(resumo[coluna_alerta])
    
    # Ordenar para ficar igual à tabela da imagem
    ordem = ["Alerta Alto", "Alerta", "Atenção", "Baixa probabilidade", "Observação"]
    resumo["ordem"] = resumo[coluna_alerta].apply(lambda x: ordem.index(x) if x in ordem else 99)
    resumo = resumo.sort_values("ordem").drop(columns="ordem")
    
    # Formatar área para ter vírgula e 3 casas decimais como na imagem
    resumo["area_km2"] = resumo["area_km2"].map(lambda x: f"{x:,.3f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    # Renomear colunas para ficar igual na tabela
    resumo = resumo.rename(columns={
        coluna_alerta: "Nível de Alerta",
        "numero_municipios": "Número de municípios",
        "area_km2": "Área (km²)"
    })
    
    # Salvar CSV
    resumo.to_csv(BASE_DIR / nome_arquivo, index=False, sep=";")
    print(f"✅ Tabela resumo salva em: {BASE_DIR / nome_arquivo}")
    
    return resumo

ufs_desejadas = ["MS", "MT", "GO", "DF"]
gdf = gpd.read_file(str(BASE_DIR) + "/NDJ_Cptec_CD_MUN_tabela_completa.shp")

# Filtrar os estados desejados
gdf_estados = gdf[gdf["SIGLA_UF"].isin(ufs_desejadas)]

# Gerar tabela
tabela_resumo = gerar_tabela_resumo(
    gdf_estados,
    coluna_alerta="alerta",  # ou "alerta_normalizado" se for o nome da sua coluna
    nome_arquivo=f"tabela_resumo_{'_'.join(ufs_desejadas)}.csv"
)