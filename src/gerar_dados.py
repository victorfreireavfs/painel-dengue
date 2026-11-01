"""Gera um CSV fictício (mas realista) de casos de dengue por estado e mês.

Os dados são FICTÍCIOS: a população é aproximada e os casos são simulados
com sazonalidade (pico no outono) e um ano epidêmico.

Como executar:  python -m src.gerar_dados
"""

import logging
import math
import random
from pathlib import Path

import pandas as pd

from src.config import (
    AMPLITUDE_SAZONAL,
    ANO_FINAL,
    ANO_INICIAL,
    ARQUIVO_DADOS,
    FATOR_EPIDEMICO_POR_ANO,
    FORMATO_LOG,
    HABITANTES_BASE_INCIDENCIA,
    LETALIDADE_BASE,
    MES_PICO,
    MESES_POR_ANO,
    PROBABILIDADE_VALOR_AUSENTE,
    QUANTIDADE_LINHAS_DUPLICADAS,
    RUIDO_MAX,
    RUIDO_MIN,
    SEMENTE_ALEATORIA,
    TAXA_BASE_MAX,
    TAXA_BASE_MIN,
)

logger = logging.getLogger(__name__)

# UF -> (região, população aproximada)
ESTADOS: dict[str, tuple[str, int]] = {
    "AC": ("Norte", 830_000), "AL": ("Nordeste", 3_127_000),
    "AP": ("Norte", 733_000), "AM": ("Norte", 3_942_000),
    "BA": ("Nordeste", 14_137_000), "CE": ("Nordeste", 8_794_000),
    "DF": ("Centro-Oeste", 2_817_000), "ES": ("Sudeste", 3_833_000),
    "GO": ("Centro-Oeste", 7_056_000), "MA": ("Nordeste", 6_776_000),
    "MT": ("Centro-Oeste", 3_658_000), "MS": ("Centro-Oeste", 2_757_000),
    "MG": ("Sudeste", 20_539_000), "PA": ("Norte", 8_121_000),
    "PB": ("Nordeste", 3_974_000), "PR": ("Sul", 11_444_000),
    "PE": ("Nordeste", 9_058_000), "PI": ("Nordeste", 3_271_000),
    "RJ": ("Sudeste", 16_055_000), "RN": ("Nordeste", 3_303_000),
    "RS": ("Sul", 10_882_000), "RO": ("Norte", 1_581_000),
    "RR": ("Norte", 636_000), "SC": ("Sul", 7_610_000),
    "SP": ("Sudeste", 44_411_000), "SE": ("Nordeste", 2_211_000),
    "TO": ("Norte", 1_511_000),
}


def _simular_casos_e_obitos(
    rng: random.Random,
    populacao: int,
    taxa_base: float,
    ano: int,
    mes: int,
) -> tuple[int, int]:
    """Simula casos e óbitos de um estado em um mês específico."""
    # Cosseno: vale 1 no mês de pico e diminui conforme nos afastamos dele.
    sazonalidade = 1 + AMPLITUDE_SAZONAL * math.cos(
        2 * math.pi * (mes - MES_PICO) / MESES_POR_ANO
    )
    fator_ano = FATOR_EPIDEMICO_POR_ANO.get(ano, 1.0)
    ruido = rng.uniform(RUIDO_MIN, RUIDO_MAX)

    casos = round(
        populacao / HABITANTES_BASE_INCIDENCIA
        * taxa_base * sazonalidade * fator_ano * ruido
    )
    obitos = round(casos * LETALIDADE_BASE * rng.uniform(RUIDO_MIN, RUIDO_MAX))
    return casos, obitos


def gerar_registros(rng: random.Random) -> list[dict[str, object]]:
    """Cria uma linha para cada combinação (estado, ano, mês)."""
    registros: list[dict[str, object]] = []
    for uf, (regiao, populacao) in ESTADOS.items():
        taxa_base = rng.uniform(TAXA_BASE_MIN, TAXA_BASE_MAX)
        for ano in range(ANO_INICIAL, ANO_FINAL + 1):
            for mes in range(1, MESES_POR_ANO + 1):
                casos, obitos = _simular_casos_e_obitos(
                    rng, populacao, taxa_base, ano, mes
                )
                # Simula falha de registro: em ~1% das linhas, casos fica vazio.
                casos_registrados = (
                    None if rng.random() < PROBABILIDADE_VALOR_AUSENTE else casos
                )
                registros.append(
                    {
                        "data": f"{ano}-{mes:02d}-01",
                        "uf": uf,
                        "regiao": regiao,
                        "populacao": populacao,
                        "casos": casos_registrados,
                        "obitos": obitos,
                    }
                )
    return registros


def gerar_dataframe(semente: int = SEMENTE_ALEATORIA) -> pd.DataFrame:
    """Gera o DataFrame completo, já com "sujeiras" propositais.

    💡 Dica: random.Random(semente) cria um gerador próprio. Com a mesma
    semente, qualquer pessoa obtém exatamente os mesmos dados (reprodutível).
    """
    rng = random.Random(semente)
    dados = pd.DataFrame(gerar_registros(rng))

    # "Int64" (com I maiúsculo) aceita inteiros E valores ausentes.
    # Sem isso o CSV sairia com "123.0" em vez de "123".
    dados["casos"] = dados["casos"].astype("Int64")

    # Dados reais quase sempre têm linhas repetidas: vamos treinar a limpeza!
    duplicadas = dados.sample(n=QUANTIDADE_LINHAS_DUPLICADAS, random_state=semente)
    return pd.concat([dados, duplicadas], ignore_index=True)


def salvar_csv(dados: pd.DataFrame, caminho: Path) -> None:
    """Salva o DataFrame em CSV, criando a pasta se necessário."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    dados.to_csv(caminho, index=False)
    logger.info("Arquivo salvo: %s (%d linhas)", caminho, len(dados))


def main() -> None:
    """Gera os dados e salva em data/raw/."""
    logging.basicConfig(level=logging.INFO, format=FORMATO_LOG)
    salvar_csv(gerar_dataframe(), ARQUIVO_DADOS)


if __name__ == "__main__":
    main()
