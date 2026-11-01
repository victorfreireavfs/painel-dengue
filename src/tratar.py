"""Camada de TRATAMENTO: limpa os dados e cria colunas úteis."""

import logging

import pandas as pd

from src.config import HABITANTES_BASE_INCIDENCIA

logger = logging.getLogger(__name__)


def tratar_dados(bruto: pd.DataFrame) -> pd.DataFrame:
    """Limpa o DataFrame bruto e devolve um novo, pronto para análise.

    Passos: remove duplicatas, padroniza textos, converte datas, descarta
    linhas sem casos e cria as colunas ano, mes e incidencia_100k.
    """
    # 💡 Dica: .copy() evita alterar o DataFrame original que veio de fora.
    dados = bruto.copy()
    total_inicial = len(dados)

    dados = dados.drop_duplicates()

    dados["uf"] = dados["uf"].str.strip().str.upper()
    dados["regiao"] = dados["regiao"].str.strip()

    # errors="coerce": datas inválidas viram NaT (ausente) em vez de quebrar.
    dados["data"] = pd.to_datetime(dados["data"], errors="coerce")

    dados = dados.dropna(subset=["data", "casos", "obitos"]).copy()
    # ⚠️ Cuidado: o .copy() acima evita o famoso SettingWithCopyWarning,
    # aviso que surge ao criar colunas em um "pedaço" de outro DataFrame.

    # Com NaN a coluna era decimal (float). Sem NaN, podemos voltar a inteiro.
    dados = dados.astype({"casos": int, "obitos": int})

    dados["ano"] = dados["data"].dt.year
    dados["mes"] = dados["data"].dt.month

    # Incidência = casos por 100 mil habitantes. Permite comparar estados
    # grandes e pequenos de forma justa.
    dados["incidencia_100k"] = (
        dados["casos"] / dados["populacao"] * HABITANTES_BASE_INCIDENCIA
    )

    logger.info(
        "Tratamento concluído: %d linhas -> %d linhas", total_inicial, len(dados)
    )
    return dados.reset_index(drop=True)
