"""Camada de ANÁLISE: funções que respondem perguntas sobre os dados.

Todas recebem um DataFrame já tratado e devolvem um resultado (nunca imprimem).
💡 Dica: funções que RETORNAM valores são fáceis de testar e de reutilizar
no gráfico, na interface e no relatório.
"""

from dataclasses import dataclass

import pandas as pd

from src.config import MESES_POR_ANO, TOP_N_PADRAO


@dataclass(frozen=True)
class Resumo:
    """Pequeno "pacote" com os números principais.

    💡 Dica: dataclass cria __init__ automaticamente. É mais claro que
    devolver um dicionário solto ou uma tupla sem nomes.
    """

    total_casos: int
    total_obitos: int
    letalidade_pct: float
    mes_pico: int | None  # None quando não há casos


def filtrar(
    dados: pd.DataFrame,
    ano: int | None = None,
    regiao: str | None = None,
) -> pd.DataFrame:
    """Filtra por ano e/ou região. Passar None significa "não filtrar"."""
    resultado = dados
    if ano is not None:
        resultado = resultado[resultado["ano"] == ano]
    if regiao is not None:
        resultado = resultado[resultado["regiao"] == regiao]
    return resultado


def casos_por_ano(dados: pd.DataFrame) -> pd.DataFrame:
    """Soma casos e óbitos de cada ano."""
    return dados.groupby("ano", as_index=False)[["casos", "obitos"]].sum()


def casos_por_mes(dados: pd.DataFrame) -> pd.Series:
    """Soma os casos de cada mês (1 a 12), somando todos os anos.

    Serve para enxergar a SAZONALIDADE: em que época do ano a doença sobe.
    """
    soma_por_mes = dados.groupby("mes")["casos"].sum()
    # reindex garante os 12 meses, mesmo que algum não tenha dados.
    return soma_por_mes.reindex(range(1, MESES_POR_ANO + 1), fill_value=0)


def top_estados_por_casos(dados: pd.DataFrame, n: int = TOP_N_PADRAO) -> pd.Series:
    """Os n estados com mais casos no total."""
    return dados.groupby("uf")["casos"].sum().sort_values(ascending=False).head(n)


def top_estados_por_incidencia(
    dados: pd.DataFrame, n: int = TOP_N_PADRAO
) -> pd.Series:
    """Os n estados com maior incidência média mensal (por 100 mil hab.).

    💡 Dica: compare com top_estados_por_casos. Estados populosos lideram em
    número ABSOLUTO, mas nem sempre em incidência. Esse é o ponto de usar
    taxas em vez de contagens brutas.
    """
    return (
        dados.groupby("uf")["incidencia_100k"]
        .mean()
        .sort_values(ascending=False)
        .head(n)
    )


def calcular_letalidade(dados: pd.DataFrame) -> float:
    """Percentual de óbitos sobre o total de casos (0.0 se não houver casos)."""
    total_casos = int(dados["casos"].sum())
    if total_casos == 0:
        return 0.0  # ⚠️ Cuidado: evita divisão por zero em filtros vazios.
    return int(dados["obitos"].sum()) / total_casos * 100


def resumir(dados: pd.DataFrame) -> Resumo:
    """Calcula os números principais de um conjunto de dados."""
    total_casos = int(dados["casos"].sum())
    mes_pico = None if total_casos == 0 else int(casos_por_mes(dados).idxmax())
    return Resumo(
        total_casos=total_casos,
        total_obitos=int(dados["obitos"].sum()),
        letalidade_pct=calcular_letalidade(dados),
        mes_pico=mes_pico,
    )
