# Visão Geral dos Scripts do Projeto `prev_prob_fogo`

Este documento serve como uma visão geral temporária dos scripts Python presentes no projeto, descrevendo suas principais funcionalidades.

---

## 1. Módulo `visualization/`

**Caminho:** `prev_prob_fogo/visualization/`

Este diretório contém os scripts responsáveis pela geração de mapas e tabelas de visualização dos dados de alerta de fogo.

### `__init__.py`
* **Propósito:** Marca o diretório `visualization` como um pacote Python. Geralmente vazio ou contendo inicializações de pacote.

### `gerar_tabela.py`
* **Propósito:** Provavelmente contém funções ou lógica para gerar dados em formato tabular ou processar dados para exibição em tabelas. Pode ser usado para pré-processar as informações antes de serem exibidas.

O script utiliza um dado estático para a localização do shapefile principal:

```python
BASE_DIR = Path("/mnt/c/Users/WHS/Documents/prev_prob_fogo/data/202411/CPTEC/")
gdf = gpd.read_file(str(BASE_DIR) + "/NDJ_Cptec_CD_MUN_tabela_completa.shp")
```

Para a Região do Centro-Oeste:

```python
ufs_desejadas = ["MS", "MT", "GO", "DF"]
```

Realizando um filtro por Estados desejados existentes dentro do arquivo NDJ_Cptec_CD_MUN_tabela_completa.shp

```python
gdf_estados = gdf[gdf["SIGLA_UF"].isin(ufs_desejadas)]
```

Utilização do método:

```python
tabela_resumo = gerar_tabela_resumo(
    gdf_estados,
    coluna_alerta="alerta",  # ou "alerta_normalizado" se for o nome da sua coluna
    nome_arquivo=f"tabela_resumo_{'_'.join(ufs_desejadas)}.csv"
)
```

Esse é o resultado com dados salvos no formato ``csv``

```python
Nível de Alerta;Número de municípios;Área (km²)
Alert;68;510.805,317
Attention;192;618.157,960
High Alert;4;114.857,646
Low Probability;47;89.844,489
Observation;156;275.454,050
```

### `listarColunasShapefile.py`
* **Propósito:** Um utilitário para inspecionar arquivos shapefile (`.shp`) e listar as colunas de atributos disponíveis neles. Útil para entender a estrutura dos dados geoespaciais.

```python
def listar_colunas_shapefile(nome_arquivo: str):
    """
    Abre um shapefile e imprime as colunas disponíveis.

    Args:
        nome_arquivo (str): Nome do arquivo .shp (ex: 'municipios.shp')
    """
```
Colunas do shapefile

```python
print(gdf.columns)
```

Primeiras linhas dos dados

```python
print(gdf.head())
```

### `plot_tabela_colorida.py`
* **Propósito:** Script dedicado à criação de tabelas visualmente aprimoradas, possivelmente com cores ou formatação condicional, para apresentar dados de alerta.

Ele tem o intuito de gerar uma taleta coloria.

Erro apresentado que requer uma atenção a mais:

```python

Traceback (most recent call last):
  File "/home/whs/.cache/pypoetry/virtualenvs/prev-prob-fogo-okXuTtb_-py3.12/lib/python3.12/site-packages/matplotlib/axes/_axes.py", line 2365, in _parse_bar_color_args
    facecolor = mcolors.to_rgba_array(facecolor)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/whs/.cache/pypoetry/virtualenvs/prev-prob-fogo-okXuTtb_-py3.12/lib/python3.12/site-packages/matplotlib/colors.py", line 515, in to_rgba_array
    rgba = np.array([to_rgba(cc) for cc in c])
                     ^^^^^^^^^^^
  File "/home/whs/.cache/pypoetry/virtualenvs/prev-prob-fogo-okXuTtb_-py3.12/lib/python3.12/site-packages/matplotlib/colors.py", line 317, in to_rgba
    rgba = _to_rgba_no_colorcycle(c, alpha)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/whs/.cache/pypoetry/virtualenvs/prev-prob-fogo-okXuTtb_-py3.12/lib/python3.12/site-packages/matplotlib/colors.py", line 401, in _to_rgba_no_colorcycle
    raise ValueError(f"Invalid RGBA argument: {orig_c!r}")
ValueError: Invalid RGBA argument: nan

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/mnt/c/Users/WHS/Documents/prev_prob_fogo/prev_prob_fogo/visualization/plot_tabela_colorida.py", line 36, in <module>
    bars1 = ax1.barh(df["Nível de Alerta"], df["Número de municípios"], color=cores)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/whs/.cache/pypoetry/virtualenvs/prev-prob-fogo-okXuTtb_-py3.12/lib/python3.12/site-packages/matplotlib/axes/_axes.py", line 2834, in barh
    patches = self.bar(x=left, height=height, width=width, bottom=y,
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/whs/.cache/pypoetry/virtualenvs/prev-prob-fogo-okXuTtb_-py3.12/lib/python3.12/site-packages/matplotlib/__init__.py", line 1521, in inner
    return func(
           ^^^^^
  File "/home/whs/.cache/pypoetry/virtualenvs/prev-prob-fogo-okXuTtb_-py3.12/lib/python3.12/site-packages/matplotlib/axes/_axes.py", line 2510, in bar
    facecolor, edgecolor = self._parse_bar_color_args(kwargs)
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/whs/.cache/pypoetry/virtualenvs/prev-prob-fogo-okXuTtb_-py3.12/lib/python3.12/site-packages/matplotlib/axes/_axes.py", line 2367, in _parse_bar_color_args
    raise ValueError(
ValueError: 'facecolor' or 'color' argument must be a valid color orsequence of colors.

```

### `plots_Estado_Centro-Oeste_borda.py`
* **Propósito:** Focado na visualização dos estados da região Centro-Oeste do Brasil (MS, MT, GO, DF), com ênfase na plotagem de suas bordas ou contornos.

    Autoexplicativo a sua utilização e dado de saída.

### `plots_Estado_Centro-Oeste_tabela_nome.py`
* **Propósito:** Similar ao anterior, mas especificamente projetado para gerar visualizações dos estados do Centro-Oeste, possivelmente incluindo nomes de municípios em uma tabela adjacente ao mapa.

Modelo elaborado utilizando o Centro-Oeste como modelo. Aplicando o contorno com espessura de 2.0 em torno de Cada Estado. Possuí uma tabela bom os ``Alerta`` e ``Alerta Alto`` registrado para os ``Estados do MS, MT, GO e DF``

```python
# Filtrar municípios em 'high alert' e 'alert'
    col_nome_mun = "NM_MUN_y"
    if col_nome_mun not in gdf_estados.columns:
        print(f"❌ Coluna '{col_nome_mun}' não encontrada no shapefile.")
        print("Colunas disponíveis:", gdf_estados.columns.tolist())
        return
    filtro_municipios = gdf_estados["alerta_normalizado"].isin(["high alert", "alert"])
    municipios_alerta = gdf_estados[filtro_municipios][[col_nome_mun, "SIGLA_UF", column, "alerta_normalizado"]].sort_values(by="alerta_normalizado")
```

```python
# Plotar as bordas dos estados com uma linha mais grossa
# Primeiro, dissolve os municípios por estado para obter os polígonos dos estados
gdf_estados_dissolved = gdf_estados.dissolve(by="SIGLA_UF")
# Depois, plota esses polígonos com uma borda mais grossa
gdf_estados_dissolved.plot(ax=ax_map, facecolor='none', edgecolor="black", linewidth=2.0) # Linha mais grossa aqui
```


### `plots_Estado_Com_Contorno_BR.py`
* **Propósito:** Gera um mapa que exibe uma seleção de estados específicos (aqueles definidos como `ufs_desejadas`) com seus dados de alerta, enquanto também mostra o contorno de todo o Brasil como contexto geográfico.

    Autoexplicativo a sua utilização e dado de saída.

### `plots_Estado_Nordeste.py`
* **Propósito:** Script dedicado à visualização dos estados da região Nordeste do Brasil, mostrando seus respectivos níveis de alerta.

    Autoexplicativo a sua utilização e dado de saída.

### `plots_Estado_NORTE-seguirEssePadrao.py`
* **Propósito:** Este script parece ser um modelo ou um exemplo de como os scripts de plotagem para as outras regiões (neste caso, o Norte) deveriam ser estruturados, seguindo um "padrão" específico de desenvolvimento ou visualização.

    Aqui tem um padrao utilizado para ajustar a legenda.

```python
# Ajuste aqui para mover a legenda:
# loc='lower left' ainda define o ponto de ancoragem da legenda (canto inferior esquerdo dela mesma)
# bbox_to_anchor=(x, y) define onde esse ponto de ancoragem será colocado no sistema de coordenadas do eixo.
# No caso de 'lower left', (0,0) é o canto inferior esquerdo do eixo.
# Ao diminuir o valor de 'y' para algo negativo (ex: -0.15), a legenda desce para fora da área do mapa.
# O valor '0' para 'x' a mantém alinhada à esquerda.
ax_map.legend(handles=legend_patches, title="Nível de Alerta", loc='lower left', bbox_to_anchor=(0, -0.15))


#ax_map.legend(handles=legend_patches, title="Nível de Alerta", loc="lower left")

```

### `plots_Estado_Sudeste.py`
* **Propósito:** Focado na visualização dos estados da região Sudeste do Brasil (SP, RJ, MG, ES) e seus dados de alerta.

Autoexplicativo a sua utilização e dado de saída.

### `plots_Estado_SUL.py`
* **Propósito:** Dedicado à visualização dos estados da região Sul do Brasil (PR, SC, RS) e seus dados de alerta.

Autoexplicativo a sua utilização e dado de saída.

### `plots_MS-v2.py`
* **Propósito:** Provavelmente uma segunda versão ou uma versão atualizada do script `plots_MS.py`, possivelmente com melhorias, correções de bugs ou novas funcionalidades específicas para o estado do Mato Grosso do Sul.

Realizando ajustes até chegar nas versões ```plots_Estado_SUL.py``` e derivados

### `plots_MS.py`
* **Propósito:** Script original para a visualização de dados de alerta para o estado do Mato Grosso do Sul.

Realizando ajustes até chegar nas versões ```plots_Estado_SUL.py``` e derivados

### `plots.py`
* **Propósito:** Um script mais genérico ou principal de plotagem. Pode ser o ponto de entrada para a geração de vários tipos de mapas ou uma função utilitária que é importada por outros scripts de `plots_Estado_...`.

---

## 2. Módulo `prev_prob_fogo_service/`

**Caminho:** `prev_prob_fogo/prev_prob_fogo_service/`

Este diretório provavelmente contém a lógica de backend ou serviços relacionados ao processamento e fornecimento dos dados de previsão de fogo.

### `__init__.py`
* **Propósito:** Marca o diretório `prev_prob_fogo_service` como um pacote Python.

### `app.py`
* **Propósito:** Comumente, este é o arquivo principal de uma aplicação web ou serviço. Pode ser onde a API REST é definida, recebendo requisições, processando dados (talvez usando os scripts de `visualization` internamente) e retornando respostas.

---