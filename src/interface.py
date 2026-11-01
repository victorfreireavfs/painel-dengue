"""Interface gráfica simples (tkinter) com filtros e gráficos embutidos.

Aqui usamos uma CLASSE porque a janela precisa "lembrar" de coisas (os dados,
o gráfico atual). Se classes são novidade, foque nos comentários.
"""

import logging
import tkinter as tk
from tkinter import messagebox, ttk

import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src.analisar import filtrar, resumir
from src.config import PASTA_SAIDA
from src.formatacao import formatar_resumo
from src.graficos import GRAFICOS, salvar_figura

logger = logging.getLogger(__name__)

OPCAO_TODOS_ANOS = "Todos"
OPCAO_TODAS_REGIOES = "Todas"
LARGURA_JANELA = 900
ALTURA_JANELA = 650
MARGEM = 10


class JanelaPrincipal(tk.Tk):
    """Janela com filtros (ano, região, tipo de gráfico) e área de gráfico."""

    def __init__(self, dados: pd.DataFrame) -> None:
        super().__init__()
        self.title("Painel de Dengue no Brasil (dados fictícios)")
        self.geometry(f"{LARGURA_JANELA}x{ALTURA_JANELA}")

        self.dados = dados
        self.figura_atual: Figure | None = None
        self.nome_arquivo_atual: str = "grafico.png"
        self.canvas: FigureCanvasTkAgg | None = None

        self._criar_widgets()
        self.atualizar()

    def _criar_combo(
        self, pai: ttk.Frame, rotulo: str, valores: list[str], largura: int
    ) -> ttk.Combobox:
        """Cria um rótulo + caixa de seleção que atualiza o gráfico ao mudar."""
        ttk.Label(pai, text=rotulo).pack(side=tk.LEFT)
        combo = ttk.Combobox(pai, values=valores, state="readonly", width=largura)
        combo.current(0)
        combo.pack(side=tk.LEFT, padx=(4, 14))
        # <<ComboboxSelected>> dispara quando o usuário escolhe uma opção.
        # O lambda ignora o "evento" que o tkinter envia e só chama atualizar.
        combo.bind("<<ComboboxSelected>>", lambda _evento: self.atualizar())
        return combo

    def _criar_widgets(self) -> None:
        barra = ttk.Frame(self, padding=MARGEM)
        barra.pack(fill=tk.X)

        anos = [OPCAO_TODOS_ANOS] + [
            str(ano) for ano in sorted(self.dados["ano"].unique())
        ]
        regioes = [OPCAO_TODAS_REGIOES] + sorted(self.dados["regiao"].unique())
        titulos = [grafico.titulo for grafico in GRAFICOS]

        self.combo_ano = self._criar_combo(barra, "Ano:", anos, 8)
        self.combo_regiao = self._criar_combo(barra, "Região:", regioes, 14)
        self.combo_grafico = self._criar_combo(barra, "Gráfico:", titulos, 28)
        ttk.Button(barra, text="Salvar PNG", command=self.salvar).pack(side=tk.LEFT)

        self.rotulo_resumo = ttk.Label(self, padding=(MARGEM, 0), justify=tk.LEFT)
        self.rotulo_resumo.pack(fill=tk.X)

        self.frame_grafico = ttk.Frame(self, padding=MARGEM)
        self.frame_grafico.pack(fill=tk.BOTH, expand=True)

    def _ano_escolhido(self) -> int | None:
        texto = self.combo_ano.get()
        return None if texto == OPCAO_TODOS_ANOS else int(texto)

    def _regiao_escolhida(self) -> str | None:
        texto = self.combo_regiao.get()
        return None if texto == OPCAO_TODAS_REGIOES else texto

    def atualizar(self) -> None:
        """Reaplica filtros, recalcula o resumo e redesenha o gráfico."""
        filtrado = filtrar(self.dados, self._ano_escolhido(), self._regiao_escolhida())
        if filtrado.empty:
            messagebox.showwarning("Sem dados", "Nenhum registro para esse filtro.")
            return

        grafico = GRAFICOS[self.combo_grafico.current()]
        self.figura_atual = grafico.construir(filtrado)
        self.nome_arquivo_atual = grafico.nome_arquivo
        self.rotulo_resumo.config(text=formatar_resumo(resumir(filtrado)))
        self._desenhar(self.figura_atual)

    def _desenhar(self, figura: Figure) -> None:
        """Troca o gráfico exibido pelo novo."""
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()  # remove o gráfico antigo
        self.canvas = FigureCanvasTkAgg(figura, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def salvar(self) -> None:
        """Salva o gráfico atual na pasta outputs/."""
        if self.figura_atual is None:
            return
        caminho = salvar_figura(
            self.figura_atual, PASTA_SAIDA / self.nome_arquivo_atual
        )
        messagebox.showinfo("Salvo", f"Gráfico salvo em:\n{caminho}")


def executar_interface(dados: pd.DataFrame) -> int:
    """Abre a janela. Retorna 0 se tudo deu certo e 1 se não foi possível abrir."""
    try:
        janela = JanelaPrincipal(dados)
    except tk.TclError as erro:
        # Acontece, por exemplo, em servidores sem tela (sem ambiente gráfico).
        logger.error("Não foi possível abrir a janela: %s", erro)
        return 1
    janela.mainloop()
    return 0
