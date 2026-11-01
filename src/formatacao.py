"""Transforma números em texto legível para o usuário."""

from src.analisar import Resumo
from src.config import NOMES_MESES


def formatar_inteiro(valor: int) -> str:
    """Formata com ponto de milhar, no padrão brasileiro: 1234567 -> 1.234.567."""
    return f"{valor:,}".replace(",", ".")


def formatar_resumo(resumo: Resumo) -> str:
    """Monta uma linha de texto com os números principais."""
    mes = "-" if resumo.mes_pico is None else NOMES_MESES[resumo.mes_pico - 1]
    return (
        f"Casos: {formatar_inteiro(resumo.total_casos)}  |  "
        f"Óbitos: {formatar_inteiro(resumo.total_obitos)}  |  "
        f"Letalidade: {resumo.letalidade_pct:.2f}%  |  "
        f"Mês de pico: {mes}"
    )
