import pandas as pd

from src.config import (
    ANO_FINAL,
    ANO_INICIAL,
    COLUNAS_OBRIGATORIAS,
    MESES_POR_ANO,
    QUANTIDADE_LINHAS_DUPLICADAS,
)
from src.gerar_dados import ESTADOS, gerar_dataframe


def test_geracao_e_reprodutivel() -> None:
    pd.testing.assert_frame_equal(gerar_dataframe(1), gerar_dataframe(1))


def test_tem_todas_as_colunas_obrigatorias() -> None:
    assert set(COLUNAS_OBRIGATORIAS) <= set(gerar_dataframe(1).columns)


def test_quantidade_de_linhas() -> None:
    anos = ANO_FINAL - ANO_INICIAL + 1
    esperado = len(ESTADOS) * MESES_POR_ANO * anos + QUANTIDADE_LINHAS_DUPLICADAS
    assert len(gerar_dataframe(1)) == esperado
