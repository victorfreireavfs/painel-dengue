"""Ponto de entrada: junta leitura, tratamento, análise, gráficos e interface.

Uso:
    python -m src.main                  # abre a interface gráfica
    python -m src.main --sem-interface  # imprime relatório e salva PNGs
"""

import argparse
import logging
from collections.abc import Sequence

import pandas as pd

from src.analisar import (
    casos_por_ano,
    resumir,
    top_estados_por_casos,
    top_estados_por_incidencia,
)
from src.carregar import carregar_csv
from src.config import ARQUIVO_DADOS, FORMATO_LOG, PASTA_SAIDA, TOP_N_PADRAO
from src.formatacao import formatar_resumo
from src.graficos import GRAFICOS, salvar_figura
from src.tratar import tratar_dados

logger = logging.getLogger(__name__)

LARGURA_RELATORIO = 64


def preparar_dados() -> pd.DataFrame:
    """Lê o CSV e devolve os dados já tratados."""
    return tratar_dados(carregar_csv(ARQUIVO_DADOS))


def imprimir_relatorio(dados: pd.DataFrame) -> None:
    """Mostra o relatório no terminal.

    💡 Dica: aqui usamos print() porque o relatório É a saída do programa
    para o usuário. Já mensagens de funcionamento ("leu arquivo", "erro")
    vão para o logging.
    """
    print("=" * LARGURA_RELATORIO)
    print("RELATÓRIO - DENGUE NO BRASIL (dados fictícios)")
    print("=" * LARGURA_RELATORIO)
    print(formatar_resumo(resumir(dados)))

    print("\nCasos e óbitos por ano:")
    print(casos_por_ano(dados).to_string(index=False))

    print(f"\nTop {TOP_N_PADRAO} estados por número de casos:")
    print(top_estados_por_casos(dados).to_string())

    print(f"\nTop {TOP_N_PADRAO} estados por incidência mensal média (por 100 mil):")
    print(top_estados_por_incidencia(dados).round(1).to_string())


def salvar_todos_graficos(dados: pd.DataFrame) -> None:
    """Gera e salva todos os gráficos em outputs/."""
    for grafico in GRAFICOS:
        figura = grafico.construir(dados)
        salvar_figura(figura, PASTA_SAIDA / grafico.nome_arquivo)


def abrir_interface(dados: pd.DataFrame) -> int:
    """Abre a janela tkinter, se o tkinter estiver disponível."""
    # 💡 Dica: importar DENTRO da função (import "preguiçoso") permite que
    # o modo --sem-interface funcione mesmo sem tkinter instalado.
    try:
        from src.interface import executar_interface
    except ImportError:
        logger.error(
            "tkinter não está instalado. Use --sem-interface "
            "ou instale o pacote python3-tk."
        )
        return 1
    return executar_interface(dados)


def ler_argumentos(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Lê as opções da linha de comando."""
    parser = argparse.ArgumentParser(description="Painel de análise de dengue.")
    parser.add_argument(
        "--sem-interface",
        action="store_true",
        help="imprime o relatório e salva os gráficos, sem abrir a janela",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Executa o programa. Retorna 0 (sucesso) ou 1 (erro)."""
    logging.basicConfig(level=logging.INFO, format=FORMATO_LOG)
    argumentos = ler_argumentos(argv)

    try:
        dados = preparar_dados()
    except (FileNotFoundError, ValueError) as erro:
        logger.error("%s", erro)
        return 1

    if argumentos.sem_interface:
        imprimir_relatorio(dados)
        salvar_todos_graficos(dados)
        return 0
    return abrir_interface(dados)


if __name__ == "__main__":
    raise SystemExit(main())
