"""Camada de LEITURA: só lê o arquivo e confere se ele tem o formato esperado."""

import logging
from pathlib import Path

import pandas as pd

from src.config import ARQUIVO_DADOS, COLUNAS_OBRIGATORIAS

logger = logging.getLogger(__name__)


def validar_colunas(dados: pd.DataFrame) -> None:
    """Levanta ValueError se faltar alguma coluna obrigatória."""
    faltantes = [col for col in COLUNAS_OBRIGATORIAS if col not in dados.columns]
    if faltantes:
        raise ValueError(f"Colunas ausentes no arquivo: {faltantes}")


def carregar_csv(caminho: Path = ARQUIVO_DADOS) -> pd.DataFrame:
    """Lê o CSV de casos de dengue e valida suas colunas.

    Raises:
        FileNotFoundError: se o arquivo não existir.
        ValueError: se o arquivo estiver vazio ou sem as colunas esperadas.
    """
    logger.info("Lendo %s", caminho)
    # 💡 Dica: capture exceções ESPECÍFICAS e devolva uma mensagem útil.
    # ⚠️ Cuidado: "except:" ou "except Exception:" esconde bugs reais.
    try:
        dados = pd.read_csv(caminho)
    except FileNotFoundError as erro:
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho}. "
            "Gere os dados com: python -m src.gerar_dados"
        ) from erro
    except pd.errors.EmptyDataError as erro:
        raise ValueError(f"O arquivo está vazio: {caminho}") from erro

    validar_colunas(dados)
    logger.info("Arquivo lido: %d linhas", len(dados))
    return dados
