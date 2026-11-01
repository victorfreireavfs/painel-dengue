"""Camada de GRÁFICOS: recebe dados tratados e devolve figuras do matplotlib.

💡 Dica: usamos Figure diretamente (e não plt.figure()). Assim o mesmo código
serve para salvar PNG e para embutir na janela tkinter, sem depender de
backends nem de janelas extras abrindo sozinhas.
"""

import logging
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from src.analisar import (
    casos_por_ano,
    casos_por_mes,
    top_estados_por_casos,
    top_estados_por_incidencia,
)
from src.config import (
    COR_PRINCIPAL,
    DPI_FIGURA,
    NOMES_MESES,
    TAMANHO_FIGURA,
    TOP_N_PADRAO,
)

logger = logging.getLogger(__name__)


def _criar_figura() -> tuple[Figure, Axes]:
    """Cria uma figura com um único eixo (a "área" onde o gráfico é desenhado)."""
    figura = Figure(figsize=TAMANHO_FIGURA, layout="constrained")
    eixo = figura.add_subplot(1, 1, 1)
    return figura, eixo


def _barras_horizontais(serie: pd.Series, titulo: str, rotulo_x: str) -> Figure:
    """Gráfico de barras horizontais (usado nos rankings de estados)."""
    figura, eixo = _criar_figura()
    # Ordem crescente: o maior valor aparece no TOPO do gráfico.
    serie.sort_values().plot(kind="barh", ax=eixo, color=COR_PRINCIPAL)
    eixo.set_title(titulo)
    eixo.set_xlabel(rotulo_x)
    eixo.set_ylabel("")
    eixo.ticklabel_format(style="plain", axis="x")  # sem notação científica
    return figura


def grafico_casos_por_ano(dados: pd.DataFrame) -> Figure:
    """Barras com o total de casos em cada ano."""
    serie = casos_por_ano(dados).set_index("ano")["casos"]
    figura, eixo = _criar_figura()
    serie.plot(kind="bar", ax=eixo, color=COR_PRINCIPAL, rot=0)
    eixo.set_title("Casos de dengue por ano")
    eixo.set_xlabel("Ano")
    eixo.set_ylabel("Casos")
    eixo.ticklabel_format(style="plain", axis="y")
    return figura


def grafico_sazonalidade(dados: pd.DataFrame) -> Figure:
    """Linha com o total de casos em cada mês do ano."""
    serie = casos_por_mes(dados)
    figura, eixo = _criar_figura()
    serie.plot(kind="line", marker="o", ax=eixo, color=COR_PRINCIPAL)
    eixo.set_xticks(range(1, len(NOMES_MESES) + 1))
    eixo.set_xticklabels(NOMES_MESES)
    eixo.set_title("Sazonalidade: casos por mês do ano")
    eixo.set_xlabel("Mês")
    eixo.set_ylabel("Casos")
    eixo.ticklabel_format(style="plain", axis="y")
    eixo.grid(alpha=0.3)
    return figura


def grafico_top_estados_casos(dados: pd.DataFrame) -> Figure:
    """Ranking de estados por número absoluto de casos."""
    return _barras_horizontais(
        top_estados_por_casos(dados),
        f"Top {TOP_N_PADRAO} estados por número de casos",
        "Casos",
    )


def grafico_top_estados_incidencia(dados: pd.DataFrame) -> Figure:
    """Ranking de estados por incidência média mensal (por 100 mil hab.)."""
    return _barras_horizontais(
        top_estados_por_incidencia(dados),
        f"Top {TOP_N_PADRAO} estados por incidência mensal média",
        "Casos por 100 mil habitantes",
    )


@dataclass(frozen=True)
class GraficoDisponivel:
    """Descreve um gráfico: nome na tela, nome do arquivo e função que o cria."""

    titulo: str
    nome_arquivo: str
    construir: Callable[[pd.DataFrame], Figure]


# 💡 Dica: uma lista de "descrições" evita if/elif gigantes. Para adicionar
# um gráfico novo, escreva a função e acrescente UMA linha aqui.
GRAFICOS: tuple[GraficoDisponivel, ...] = (
    GraficoDisponivel("Casos por ano", "casos_por_ano.png", grafico_casos_por_ano),
    GraficoDisponivel(
        "Sazonalidade (casos por mês)", "sazonalidade.png", grafico_sazonalidade
    ),
    GraficoDisponivel(
        "Top estados por casos", "top_estados_casos.png", grafico_top_estados_casos
    ),
    GraficoDisponivel(
        "Top estados por incidência",
        "top_estados_incidencia.png",
        grafico_top_estados_incidencia,
    ),
)


def salvar_figura(figura: Figure, caminho: Path) -> Path:
    """Salva a figura como PNG, criando a pasta se necessário."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(caminho, dpi=DPI_FIGURA)
    logger.info("Gráfico salvo: %s", caminho)
    return caminho
