"""Fixtures: dados pequenos e controlados, compartilhados entre os testes.

💡 Dica: testes usam dados MINÚSCULOS cujo resultado você calcula de cabeça.
Assim, se o teste falhar, o erro está no código, não nos dados.
"""

import pandas as pd
import pytest

from src.tratar import tratar_dados


@pytest.fixture
def df_bruto() -> pd.DataFrame:
    """4 linhas com sujeiras: espaço/minúscula em 'uf', duplicata e casos vazio."""
    return pd.DataFrame(
        {
            "data": ["2024-01-01", "2024-02-01", "2024-02-01", "2024-03-01"],
            "uf": [" pe", "SP", "SP", "SP"],
            "regiao": ["Nordeste", "Sudeste", "Sudeste", "Sudeste"],
            "populacao": [1_000_000, 2_000_000, 2_000_000, 2_000_000],
            "casos": [100, 200, 200, None],
            "obitos": [1, 2, 2, 0],
        }
    )


@pytest.fixture
def df_tratado(df_bruto: pd.DataFrame) -> pd.DataFrame:
    """Resultado esperado: 2 linhas (PE em janeiro e SP em fevereiro)."""
    return tratar_dados(df_bruto)
