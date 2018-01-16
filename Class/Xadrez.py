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
        self.jogadas = list()  # jogadas = [[oi, oj], [ni, nj]] ou [[i, j], acao]

        self.__tabuleiro = [[None] * 8 for _ in range(8)]

        self.reposicionar_pecas()

        self.tornar_matriz_legivel = lambda array: numpy.rot90(array, 3).tolist()
        self.tornar_posicao_logica = lambda pos: [7 - pos[1], pos[0]]

    def reposicionar_pecas(self):
        self.__tabuleiro = [[None] * 8 for _ in range(8)]

        self.__tabuleiro[0][0] = Torre(self.__branco)
        self.__tabuleiro[0][1] = Cavalo(self.__branco)
        self.__tabuleiro[0][2] = Bispo(self.__branco)
        self.__tabuleiro[0][3] = Rainha(self.__branco)
        self.__tabuleiro[0][4] = Rei(self.__branco)
        self.__tabuleiro[0][5] = Bispo(self.__branco)
        self.__tabuleiro[0][6] = Cavalo(self.__branco)
        self.__tabuleiro[0][7] = Torre(self.__branco)

        self.__tabuleiro[1][0] = Peao(self.__branco)
        self.__tabuleiro[1][1] = Peao(self.__branco)
        self.__tabuleiro[1][2] = Peao(self.__branco)
        self.__tabuleiro[1][3] = Peao(self.__branco)
        self.__tabuleiro[1][4] = Peao(self.__branco)
        self.__tabuleiro[1][5] = Peao(self.__branco)
        self.__tabuleiro[1][6] = Peao(self.__branco)
        self.__tabuleiro[1][7] = Peao(self.__branco)

        self.__tabuleiro[7][0] = Torre(self.__preto)
        self.__tabuleiro[7][1] = Cavalo(self.__preto)
        self.__tabuleiro[7][2] = Bispo(self.__preto)
        self.__tabuleiro[7][3] = Rainha(self.__preto)
        self.__tabuleiro[7][4] = Rei(self.__preto)
        self.__tabuleiro[7][5] = Bispo(self.__preto)
        self.__tabuleiro[7][6] = Cavalo(self.__preto)
        self.__tabuleiro[7][7] = Torre(self.__preto)

        self.__tabuleiro[6][0] = Peao(self.__preto)
        self.__tabuleiro[6][1] = Peao(self.__preto)
        self.__tabuleiro[6][2] = Peao(self.__preto)
        self.__tabuleiro[6][3] = Peao(self.__preto)
        self.__tabuleiro[6][4] = Peao(self.__preto)
        self.__tabuleiro[6][5] = Peao(self.__preto)
        self.__tabuleiro[6][6] = Peao(self.__preto)
        self.__tabuleiro[6][7] = Peao(self.__preto)

        self.vez = True
        self.jogadas = list()

    def desfazer(self, num=1):
        jogadas = self.jogadas[:-num]
        self.reposicionar_pecas()
        for jogada in jogadas:
            old, new = jogada
            old_linha, old_coluna = old
            if isinstance(old, list):
                new_linha, new_coluna = new
                self.__tabuleiro[new_linha][new_coluna] = self.__tabuleiro[old_linha][old_coluna]
                self.__tabuleiro[old_linha][old_coluna] = None
                self.vez = not self.vez
            else:
                if new == 'enpassant':
                    self.__tabuleiro[old_linha][old_coluna] = None
                elif new == 'Rainha':
                    self.__tabuleiro[old_linha][old_coluna] = Rainha(self.vez)
                elif new == 'Torre':
                    self.__tabuleiro[old_linha][old_coluna] = Torre(self.vez)
                elif new == 'Bispo':
                    self.__tabuleiro[old_linha][old_coluna] = Bispo(self.vez)
                elif new == 'Cavalo':
                    self.__tabuleiro[old_linha][old_coluna] = Cavalo(self.vez)
                else:
                    self.__tabuleiro[old_linha][old_coluna] = Peao(self.vez)
        self.jogadas = jogadas

    # posicao = [i, j]
    def movimentar_peca(self, old_posicao, new_posicao):
        old_linha, old_coluna = old_posicao
        l_old_linha, l_old_coluna = l_old_posicao = self.tornar_posicao_logica(old_posicao)
        l_new_linha, l_new_coluna = l_new_posicao = self.tornar_posicao_logica(new_posicao)
        peca = self.tabuleiro[old_linha][old_coluna]
        if peca:
            if peca.cor == self.vez:
                movimentavel = peca.movimento(
                    self.__tabuleiro,
                    [l_old_linha, l_old_coluna],
                    self.tornar_posicao_logica(new_posicao)
                )
                if movimentavel:
                    self.__tabuleiro[l_new_linha][l_new_coluna] = self.__tabuleiro[l_old_linha][l_old_coluna]
                    self.__tabuleiro[l_old_linha][l_old_coluna] = None
                    self.jogadas.append([l_old_posicao, l_new_posicao])
                    print(f'{l_old_posicao} -> {l_new_posicao}')
                    # Se for uma promoção ou o en passant:
                    if isinstance(movimentavel, tuple) or isinstance(movimentavel, list):
                        acao, comando = movimentavel
                        if acao == 'enpassant':
                            i, j = comando
                            print('en passant')
                            self.__tabuleiro[i][j] = None
                            self.jogadas.append(l_old_posicao, 'enpassant')
                        elif acao == 'promocao':
                            return 'promocao'  # A vez não foi alterada

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
        i, j = self.tornar_posicao_logica(posicao)
        self.__tabuleiro[i][j] = peca
        self.jogadas.append([[i, j], nome])
        print(f'[{i}, {j}] -> {nome}')
        self.vez = not self.vez  # Altera a vez que não foi alterada no metodo movimentar_peca

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
            movimentos = [[False] * 8 for _ in range(8)]

        return self.tornar_matriz_legivel(movimentos)
