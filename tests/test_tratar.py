import pandas as pd
import pytest

from src.carregar import validar_colunas
from src.tratar import tratar_dados


def test_remove_duplicadas_e_linhas_sem_casos(df_tratado: pd.DataFrame) -> None:
    assert len(df_tratado) == 2


def test_padroniza_uf(df_tratado: pd.DataFrame) -> None:
    assert set(df_tratado["uf"]) == {"PE", "SP"}


def test_calcula_incidencia_por_100_mil(df_tratado: pd.DataFrame) -> None:
    linha_pe = df_tratado[df_tratado["uf"] == "PE"].iloc[0]
    # 100 casos / 1.000.000 hab. * 100.000 = 10 casos por 100 mil
    assert linha_pe["incidencia_100k"] == pytest.approx(10.0)


def test_cria_colunas_ano_e_mes(df_tratado: pd.DataFrame) -> None:
    assert {"ano", "mes"} <= set(df_tratado.columns)
    assert set(df_tratado["ano"]) == {2024}


def test_validar_colunas_levanta_erro_quando_faltam_colunas() -> None:
    incompleto = pd.DataFrame({"data": ["2024-01-01"]})
    with pytest.raises(ValueError):
        validar_colunas(incompleto)
