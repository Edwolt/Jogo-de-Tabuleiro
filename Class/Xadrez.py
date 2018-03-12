import numpy

from Class.PecasXadrez import *


class Xadrez:
    """Retém o tabuleiro e informações sobre o jogo"""

    @property
    def tabuleiro(self):
        """Retorna o tabuleiro de forma que uma View consiga exibi-lo corretamente"""

        return numpy.rot90(self.__tabuleiro, 3).tolist()

    def __init__(self):
        self.vez = True  # True significa vez das peças brancas e False das pretas
        self.jogadas = list()  # jogada = [(old_i, old_j, (new_i, new_j)] ou [(i, j), acao]

        self.__tabuleiro = [[None] * 8 for _ in range(8)]  # Tabuleiro vazio

        self.reposicionar_pecas()  # self.__tabuleiro fica com o tabuleiro pronto para começar uma partida

        self.tornar_posicao_logica = lambda pos: (7 - pos[1], pos[0])  # Torne a posição fácil de ser usada em Xadrez

    def reposicionar_pecas(self):
        """Coloque as peças nas posições do inicio da partida"""

        self.__tabuleiro = [[None] * 8 for _ in range(8)]

        # Brancos
        self.__tabuleiro[0][0] = Torre(True)
        self.__tabuleiro[0][1] = Cavalo(True)
        self.__tabuleiro[0][2] = Bispo(True)
        self.__tabuleiro[0][3] = Rainha(True)
        self.__tabuleiro[0][4] = Rei(True)
        self.__tabuleiro[0][5] = Bispo(True)
        self.__tabuleiro[0][6] = Cavalo(True)
        self.__tabuleiro[0][7] = Torre(True)
        for i in range(8):  # Peões brancos
            self.__tabuleiro[1][i] = Peao(True)

        # Pretos
        self.__tabuleiro[7][0] = Torre(False)
        self.__tabuleiro[7][1] = Cavalo(False)
        self.__tabuleiro[7][2] = Bispo(False)
        self.__tabuleiro[7][3] = Rainha(False)
        self.__tabuleiro[7][4] = Rei(False)
        self.__tabuleiro[7][5] = Bispo(False)
        self.__tabuleiro[7][6] = Cavalo(False)
        self.__tabuleiro[7][7] = Torre(False)
        for i in range(8):  # Peões pretos
            self.__tabuleiro[6][i] = Peao(False)

        self.vez = True  # Vez das peças brancas
        self.jogadas.clear()  # Limpa todas as jogadas

    def movimentar_peca(self, old_posicao: tuple, new_posicao: tuple):
        """
        Movimente uma peca de old_posicao para new_posicao

        :param old_posicao: [i, j]
        :param new_posicao: [i, j]
        :return: None, mas pode retorna 'promoção' se for o caso
        """

        old_linha, old_coluna = old_posicao
        l_old_linha, l_old_coluna = l_old_posicao = self.tornar_posicao_logica(old_posicao)
        l_new_linha, l_new_coluna = l_new_posicao = self.tornar_posicao_logica(new_posicao)
        peca = self.tabuleiro[old_linha][old_coluna]
        if peca:  # Se tiver uma peça
            if peca.cor == self.vez:  # Se for a vez dessa peça
                movimentavel = peca.movimento(
                    self.__tabuleiro,
                    (l_old_linha, l_old_coluna),
                    self.tornar_posicao_logica(new_posicao)
                )  # Ve se é possivel movimentar, se for True a peça considera que o movimento com certeza acontecerá
                if movimentavel:
                    self.__tabuleiro[l_new_linha][l_new_coluna] = self.__tabuleiro[l_old_linha][l_old_coluna]
                    self.__tabuleiro[l_old_linha][l_old_coluna] = None
                    self.jogadas.append((l_old_posicao, l_new_posicao))  # Guarda jogada
                    print(f'{l_old_posicao} -> {l_new_posicao}')

                    # Se for uma promoção ou o en passant o movimentavel sera um valor diferente de bool
                    if isinstance(movimentavel, (tuple, list)):
                        acao, comando = movimentavel
                        if acao == 'promocao':
                            return 'promocao'  # Retorna que está havendo uma promoção para ViewXadrez
                            # A vez não foi alterada

                        elif acao == 'enpassant':
                            i, j = comando
                            print('en passant')
                            self.__tabuleiro[i][j] = None
                            self.jogadas.append((l_old_posicao, 'enpassant'))  # Guarda jogada como movimento especial

                        elif False:  # TODO Roque
                            pass

                    self.vez = not self.vez

    def get_movimentos(self, linha: int, coluna: int):
        """
        :return: list 8x8 com os movimentos possiveis para ser usada em uma View
        """

        peca = self.tabuleiro[linha][coluna]
        if peca.cor == self.vez:  # Se a vez permitir a peça mover
            # Se a peca que movimentou for um Peao e ela já movimentou:
            if isinstance(peca, Peao) and peca.movimentou:  # Se a peça for um Peao
                ultima_jogada = self.jogadas[-1]  # Última jogada feita
                if not isinstance(ultima_jogada[1], str):  # Se ultima jogada for um movimento normal
                    peca.enpassant = ultima_jogada  # O Peao deve verificar a possibilidade de um enpassant

            movimentos = peca.get_movimentos(
                self.__tabuleiro,
                self.tornar_posicao_logica((linha, coluna)),
            )  # Movimentos possíveis
        else:  # Se não for a vez da peça
            movimentos = [[False] * 8 for _ in range(8)]  # Não há movimentos possíveis

        return numpy.rot90(movimentos, 3).tolist()  # Torna a posição fácil de ser usada em uma View

    # TODO Roque

    def promocao(self, nome: str, posicao: tuple):
        """
        Promove um Peao

        :param nome: Nome da peça para qual o Peao será promovido (deve ser igual o nome das classes)
        :param posicao: (i, j)
        :raise: Raise um Exception quando o nome da pe;a não estiver correto
        """

        i, j = self.tornar_posicao_logica(posicao)

        if nome == 'Rainha':
            self.__tabuleiro[i][j] = Rainha(self.vez)
        elif nome == 'Torre':
            self.__tabuleiro[i][j] = Torre(self.vez)
        elif nome == 'Bispo':
            self.__tabuleiro[i][j] = Bispo(self.vez)
        elif nome == 'Cavalo':
            self.__tabuleiro[i][j] = Cavalo(self.vez)
        else:
            raise Exception(f'Peça {nome} não foi encontrada e por isso não foi possivel a promoção')

        self.jogadas.append(((i, j), nome))
        print(f'{self.jogadas[-1][0]} -> {nome}')
        self.vez = not self.vez  # Altera a vez que não foi alterada no metodo movimentar_peca

    def desfazer(self, num: int = 1):
        """
        Volte o jogo à {num} jogadas atrás

        :param num: numéro de jogadas a ser voltadas
        """

        jogadas = self.jogadas[:-num]  # Pega todas as jogadas do inicio ate num vezes antes do total
        self.reposicionar_pecas()
        for jogada in jogadas:  # Todas jogadas são refeitas até que chegue uma jogada antes da que queria ser desfeita
            old, new = jogada
            old_linha, old_coluna = old
            if isinstance(old, (tuple, list)):  # Movimento normal
                new_linha, new_coluna = new

                # Faz movimento
                self.__tabuleiro[new_linha][new_coluna] = self.__tabuleiro[old_linha][old_coluna]
                self.__tabuleiro[old_linha][old_coluna] = None

                self.vez = not self.vez  # Altera a vez

            else:  # Movimento especial
                if new == 'Rainha':  # Bloco de Promoção
                    self.__tabuleiro[old_linha][old_coluna] = Rainha(self.vez)
                elif new == 'Torre':
                    self.__tabuleiro[old_linha][old_coluna] = Torre(self.vez)
                elif new == 'Bispo':
                    self.__tabuleiro[old_linha][old_coluna] = Bispo(self.vez)
                elif new == 'Cavalo':
                    self.__tabuleiro[old_linha][old_coluna] = Cavalo(self.vez)
                elif new == 'enpassant':  # Enpassant
                    self.__tabuleiro[old_linha][old_coluna] = None
                else:
                    raise Exception(f'O movimento {old} -> {new} não pode ser feito')
        self.jogadas = jogadas  # self.jogadas recebe as jogadas feitas antes das jogadas desfeitas
