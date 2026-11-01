"""Configurações centrais do projeto.

💡 Dica: concentrar constantes aqui evita "números mágicos" espalhados pelo
código. Se precisar mudar algo (ex.: o ano final), muda em UM lugar só.
"""

from pathlib import Path

# --- Caminhos -------------------------------------------------------------
# 💡 Dica: pathlib monta caminhos que funcionam em Windows, Linux e macOS.
# Nunca escreva "data\\raw\\arquivo.csv" como texto: quebra em outros sistemas.
RAIZ_PROJETO: Path = Path(__file__).resolve().parent.parent
PASTA_DADOS_BRUTOS: Path = RAIZ_PROJETO / "data" / "raw"
PASTA_SAIDA: Path = RAIZ_PROJETO / "outputs"
ARQUIVO_DADOS: Path = PASTA_DADOS_BRUTOS / "casos_dengue.csv"

# --- Estrutura esperada do CSV --------------------------------------------
COLUNAS_OBRIGATORIAS: tuple[str, ...] = (
    "data",
    "uf",
    "regiao",
    "populacao",
    "casos",
    "obitos",
)

# --- Constantes de análise ------------------------------------------------
HABITANTES_BASE_INCIDENCIA: int = 100_000  # incidência é medida "por 100 mil hab."
TOP_N_PADRAO: int = 10
MESES_POR_ANO: int = 12
NOMES_MESES: tuple[str, ...] = (
    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
    "Jul", "Ago", "Set", "Out", "Nov", "Dez",
)

# --- Geração dos dados fictícios ------------------------------------------
SEMENTE_ALEATORIA: int = 42          # mesma semente = mesmos dados sempre
ANO_INICIAL: int = 2022
ANO_FINAL: int = 2025
TAXA_BASE_MIN: float = 15.0          # casos/100 mil/mês (média do estado)
TAXA_BASE_MAX: float = 80.0
MES_PICO: int = 4                    # dengue costuma pico em março/abril
AMPLITUDE_SAZONAL: float = 0.8       # quão forte é a sazonalidade (0 a 1)
RUIDO_MIN: float = 0.7               # variação aleatória mensal
RUIDO_MAX: float = 1.3
LETALIDADE_BASE: float = 0.0006      # ~0,06% dos casos evoluem a óbito
PROBABILIDADE_VALOR_AUSENTE: float = 0.01
QUANTIDADE_LINHAS_DUPLICADAS: int = 5
# Anos "epidêmicos" multiplicam os casos. Anos fora do dicionário usam 1.0.
FATOR_EPIDEMICO_POR_ANO: dict[int, float] = {
    2022: 1.0,
    2023: 1.3,
    2024: 3.0,
    2025: 1.2,
}

# --- Gráficos e logs ------------------------------------------------------
TAMANHO_FIGURA: tuple[float, float] = (8.0, 4.5)
DPI_FIGURA: int = 120
COR_PRINCIPAL: str = "#2a6f97"
FORMATO_LOG: str = "%(asctime)s | %(levelname)-7s | %(message)s"
