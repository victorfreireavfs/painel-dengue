import pandas as pd
import pytest

from src.analisar import (
    calcular_letalidade,
    casos_por_ano,
    casos_por_mes,
    filtrar,
    resumir,
    top_estados_por_casos,
)


def test_casos_por_ano_soma_corretamente(df_tratado: pd.DataFrame) -> None:
    resultado = casos_por_ano(df_tratado)
    assert resultado.loc[0, "ano"] == 2024
    assert resultado.loc[0, "casos"] == 300


def test_casos_por_mes_tem_12_meses(df_tratado: pd.DataFrame) -> None:
    serie = casos_por_mes(df_tratado)
    assert len(serie) == 12
    assert serie[1] == 100
    assert serie[2] == 200


def test_top_estados_ordena_do_maior_para_o_menor(df_tratado: pd.DataFrame) -> None:
    assert top_estados_por_casos(df_tratado, n=1).index[0] == "SP"


def test_filtrar_por_regiao(df_tratado: pd.DataFrame) -> None:
    assert len(filtrar(df_tratado, regiao="Nordeste")) == 1


def test_letalidade(df_tratado: pd.DataFrame) -> None:
    # 3 óbitos / 300 casos * 100 = 1%
    assert calcular_letalidade(df_tratado) == pytest.approx(1.0)


def test_resumo_de_filtro_vazio_nao_quebra(df_tratado: pd.DataFrame) -> None:
    vazio = filtrar(df_tratado, ano=1999)
    resumo = resumir(vazio)
    assert resumo.total_casos == 0
    assert resumo.letalidade_pct == 0.0
    assert resumo.mes_pico is None


def test_resumo_normal(df_tratado: pd.DataFrame) -> None:
    resumo = resumir(df_tratado)
    assert resumo.total_casos == 300
    assert resumo.mes_pico == 2
