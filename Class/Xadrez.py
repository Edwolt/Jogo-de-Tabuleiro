import numpy

from Class.PecasXadrez import *


class Xadrez:
    @property
    def tabuleiro(self):
        return self.tornar_matriz_legivel(self.__tabuleiro)

    def __init__(self, branco=True, preto=False):
        self.__preto = preto
        self.__branco = branco
        self.vez = True
        self.jogadas = list()

        tabuleiro = [None] * 8
        for i, _ in enumerate(tabuleiro):
            tabuleiro[i] = [None] * 8
        self.__tabuleiro = tabuleiro

        self.reposicionar_pecas()

        self.tornar_matriz_legivel = lambda array: numpy.rot90(array, 3).tolist()
        self.tornar_posicao_logica = lambda pos: [7 - pos[1], pos[0]]

    def reposicionar_pecas(self):
        tabuleiro = [None] * 8
        for i, _ in enumerate(tabuleiro):
            tabuleiro[i] = [None] * 8
        self.__tabuleiro = tabuleiro

        self.posicionar_peca(Torre(self.__branco), [0, 0])
        self.posicionar_peca(Cavalo(self.__branco), [0, 1])
        self.posicionar_peca(Bispo(self.__branco), [0, 2])
        self.posicionar_peca(Rainha(self.__branco), [0, 3])
        self.posicionar_peca(Rei(self.__branco), [0, 4])
        self.posicionar_peca(Bispo(self.__branco), [0, 5])
        self.posicionar_peca(Cavalo(self.__branco), [0, 6])
        self.posicionar_peca(Torre(self.__branco), [0, 7])

        self.posicionar_peca(Peao(self.__branco), [1, 0])
        self.posicionar_peca(Peao(self.__branco), [1, 1])
        self.posicionar_peca(Peao(self.__branco), [1, 2])
        self.posicionar_peca(Peao(self.__branco), [1, 3])
        self.posicionar_peca(Peao(self.__branco), [1, 4])
        self.posicionar_peca(Peao(self.__branco), [1, 5])
        self.posicionar_peca(Peao(self.__branco), [1, 6])
        self.posicionar_peca(Peao(self.__branco), [1, 7])

        self.posicionar_peca(Torre(self.__preto), [7, 0])
        self.posicionar_peca(Cavalo(self.__preto), [7, 1])
        self.posicionar_peca(Bispo(self.__preto), [7, 2])
        self.posicionar_peca(Rainha(self.__preto), [7, 3])
        self.posicionar_peca(Rei(self.__preto), [7, 4])
        self.posicionar_peca(Bispo(self.__preto), [7, 5])
        self.posicionar_peca(Cavalo(self.__preto), [7, 6])
        self.posicionar_peca(Torre(self.__preto), [7, 7])

        self.posicionar_peca(Peao(self.__preto), [6, 0])
        self.posicionar_peca(Peao(self.__preto), [6, 1])
        self.posicionar_peca(Peao(self.__preto), [6, 2])
        self.posicionar_peca(Peao(self.__preto), [6, 3])
        self.posicionar_peca(Peao(self.__preto), [6, 4])
        self.posicionar_peca(Peao(self.__preto), [6, 5])
        self.posicionar_peca(Peao(self.__preto), [6, 6])
        self.posicionar_peca(Peao(self.__preto), [6, 7])

        self.vez = True

    # Posicao = '1A', '2C', etc,
    def posicionar_peca(self, peca, posicao):
        linha, coluna = posicao
        self.__tabuleiro[linha][coluna] = peca

    # posicao = [i, j]
    def movimentar_peca(self, old_posicao, new_posicao):
        old_linha, old_coluna = old_posicao
        l_old_linha, l_old_coluna = l_old_posicao = self.tornar_posicao_logica(old_posicao)
        l_new_posicao = self.tornar_posicao_logica(new_posicao)
        peca = self.tabuleiro[old_linha][old_coluna]
        if peca:
            if peca.cor == self.vez:
                movimentavel = peca.movimento(
                    self.__tabuleiro,
                    [l_old_linha, l_old_coluna],
                    self.tornar_posicao_logica(new_posicao)
                )
                if movimentavel:
                    self.posicionar_peca(self.__tabuleiro[l_old_linha][l_old_coluna], l_new_posicao)
                    self.posicionar_peca(None, l_old_posicao)
                    self.jogadas.append([l_old_posicao, l_new_posicao])
                    print(f'{l_old_posicao} -> {l_new_posicao}')
                    # Se for um movimento especial como o enpassant:
                    if isinstance(movimentavel, tuple) or isinstance(movimentavel, list):
                        acao, comando = movimentavel
                        if acao == 'enpassant':
                            self.posicionar_peca(None, comando)
                        elif acao == 'promocao':
                            return 'promocao'

                    self.vez = not self.vez

    def promocao(self, nome, posicao):
        if nome == 'Rainha':
            peca = Rainha(self.vez)
        elif nome == 'Torre':
            peca = Torre(self.vez)
        elif nome == 'Bispo':
            peca = Bispo(self.vez)
        elif nome == 'Cavalo':
            peca = Cavalo(self.vez)
        else:
            peca = Peao(self.vez)
        self.posicionar_peca(peca, self.tornar_posicao_logica(posicao))
        self.vez = not self.vez

    def get_movimentos(self, linha, coluna):
        peca = self.tabuleiro[linha][coluna]
        if peca.cor == self.vez:
            # Se a peca que movimentou for um Peao e ela ainda não tivesse movimentado:
            if isinstance(peca, Peao) and peca.movimentou:
                peca.enpassant = self.jogadas[len(self.jogadas) - 1]

            movimentos = peca.get_movimentos(
                self.__tabuleiro,
                self.tornar_posicao_logica([linha, coluna]),
            )
        else:
            movimentos = [[False]]

        return self.tornar_matriz_legivel(movimentos)
