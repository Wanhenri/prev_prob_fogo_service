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

    # Filtrar municípios em 'high alert' e 'alert'
    col_nome_mun = "NM_MUN_y"
    if col_nome_mun not in gdf_estados.columns:
        print(f"❌ Coluna '{col_nome_mun}' não encontrada no shapefile.")
        print("Colunas disponíveis:", gdf_estados.columns.tolist())
        return
    #filtro_municipios = gdf_estados["alerta_normalizado"].isin(["high alert", "alert"])
    filtro_municipios = gdf_estados["alerta_normalizado"].isin(["high alert"])
    municipios_alerta = gdf_estados[filtro_municipios][[col_nome_mun, "SIGLA_UF", column, "alerta_normalizado"]].sort_values(by="alerta_normalizado")

    # Layout com 2 colunas: mapa + tabela
    #SUDESTE
    fig = plt.figure(figsize=(28, 28))
    spec = gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[3, 1]) # Ajustei a proporção para o mapa ser maior
    ax_map = fig.add_subplot(spec[0])
    ax_table = fig.add_subplot(spec[1])

    # Plot do mapa
    gdf_estados.plot(ax=ax_map, color=gdf_estados["cor"], edgecolor="black", linewidth=0.5)

    # Plotar as bordas dos estados com uma linha mais grossa
    # Primeiro, dissolve os municípios por estado para obter os polígonos dos estados
    gdf_estados_dissolved = gdf_estados.dissolve(by="SIGLA_UF")
    # Depois, plota esses polígonos com uma borda mais grossa
    gdf_estados_dissolved.plot(ax=ax_map, facecolor='none', edgecolor="black", linewidth=2.0) # Linha mais grossa aqui

    ax_map.set_title(title, fontsize=16)
    ax_map.axis("off")

    # Legenda personalizada
    if ordem_legenda:
        categorias_legenda = [c for c in ordem_legenda if c in gdf_estados["alerta_normalizado"].unique()]
    else:
        categorias_legenda = sorted(gdf_estados["alerta_normalizado"].unique())

    legend_patches = [
        mpatches.Patch(color=ALERTA_CORES.get(cat, COR_DEFAULT), label=ALERTA_TRADUZIDO.get(cat, cat))
        for cat in categorias_legenda
    ]

    # Ajuste aqui para mover a legenda:
    # loc='lower left' ainda define o ponto de ancoragem da legenda (canto inferior esquerdo dela mesma)
    # bbox_to_anchor=(x, y) define onde esse ponto de ancoragem será colocado no sistema de coordenadas do eixo.
    # No caso de 'lower left', (0,0) é o canto inferior esquerdo do eixo.
    # Ao diminuir o valor de 'y' para algo negativo (ex: -0.15), a legenda desce para fora da área do mapa.
    # O valor '0' para 'x' a mantém alinhada à esquerda.
    ax_map.legend(handles=legend_patches, title="Nível de Alerta", loc='lower left', bbox_to_anchor=(0, -0.15))


    #ax_map.legend(handles=legend_patches, title="Nível de Alerta", loc="lower right")

    # Tabela lateral com municípios em alerta
    ax_table.axis("off")
    ax_table.set_title("Municípios com alto risco", fontsize=14, pad=10)

    if not municipios_alerta.empty:
        nomes_municipios = [
            f"{row[col_nome_mun]} ({row['SIGLA_UF']}) - {ALERTA_TRADUZIDO.get(row['alerta_normalizado'], row['alerta_normalizado'])}"
            for _, row in municipios_alerta.iterrows()
        ]
        colunas = 1 if len(nomes_municipios) <= 30 else 2
        col_len = (len(nomes_municipios) + colunas - 1) // colunas
        texto = ""
        for i in range(col_len):
            linha = ""
            for j in range(colunas):
                idx = i + j * col_len
                if idx < len(nomes_municipios):
                    linha += f"{nomes_municipios[idx]:<45} "
            texto += linha + "\n"
        ax_table.text(0, 1, texto, va='top', ha='left', fontsize=10, family="monospace")
    else:
        ax_table.text(0.5, 0.5, "Nenhum município em 'Alerta Alto' ou 'Alerta'.", va='center', ha='center', fontsize=12)

    plt.tight_layout()

    # Salvar imagem
    estados_nome = "_".join(ufs)
    output_path = BASE_DIR / f"mapa_{estados_nome}_alerta.png"
    plt.savefig(output_path, dpi=300)
    print(f"✅ Mapa com tabela salvo em: {output_path}")
    plt.show()

    # Salvar CSV
    if not municipios_alerta.empty:
        tabela_csv_path = BASE_DIR / f"municipios_high_alert_alert_{estados_nome}.csv"
        municipios_alerta.to_csv(tabela_csv_path, index=False)
        print(f"✅ CSV salvo em: {tabela_csv_path}")
    else:
        print("\nℹ️ Nenhum município com 'Alerta Alto' ou 'Alerta' para salvar no CSV.")

    # Impressão no terminal
    for nivel in ["high alert", "alert"]:
        lista = municipios_alerta[municipios_alerta["alerta_normalizado"] == nivel]
        nomes = sorted(lista[col_nome_mun].unique())
        print(f"\n🔴 Municípios em '{ALERTA_TRADUZIDO.get(nivel)}':")
        if nomes:
            for nome in nomes:
                print(f"- {nome}")
        else:
            print("Nenhum.")

    # Supondo que o código do município esteja na coluna 'CD_MUN'
    col_codigo_mun = "CD_MUN"  

    if col_codigo_mun not in gdf_estados.columns:
        print(f"⚠️ Coluna '{col_codigo_mun}' não encontrada no shapefile. Salvando CSV sem o código do município.")
        colunas_csv = [col_nome_mun, "SIGLA_UF", column, "alerta_normalizado"]
    else:
        colunas_csv = [col_codigo_mun, col_nome_mun, "SIGLA_UF", column, "alerta_normalizado"]

    # Alterar aqui a criação do DataFrame municipios_alerta para incluir código do município:
    municipios_alerta = gdf_estados[filtro_municipios][colunas_csv].sort_values(by="alerta_normalizado")

    # Ao salvar CSV:
    tabela_csv_path = BASE_DIR / f"municipios_high_alert_alert_{estados_nome}.csv"
    municipios_alerta.to_csv(tabela_csv_path, index=False)
    print(f"✅ CSV salvo em: {tabela_csv_path}")


if __name__ == "__main__":
    ufs_desejadas = ["MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"]
    ordem_personalizada = ["high alert", "alert", "attention", "observation","low probability" ]
    plotar_estados(
        filename="NDJ_Cptec_CD_MUN_tabela_completa.shp",
        ufs=ufs_desejadas,
        title="Mapa de Alerta - Estados do Nordeste",
        ordem_legenda=ordem_personalizada
    )
