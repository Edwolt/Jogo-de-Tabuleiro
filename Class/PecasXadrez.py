"""Contém classes de peças para o jogo de Xadrez e métodos relativas as peças"""


def nome_pecas() -> tuple:
    """:return: list com o nome de todas as peças do Xadrez"""

    # Coisas que estão presentes em PecasXadrez.__dict__ e que não são peças
    special_dicts = [
        '__name__',
        '__doc__',
        '__package__',
        '__loader__',
        '__spec__',
        '__file__',
        '__cached__',
        '__builtins__',
        'nome_pecas',
        'tabuleiro_vazio'
    ]

    from Class import PecasXadrez
    # peças e uma lista de dicts desse arquivo que não estão em special_dicts
    pecas = (i for i in PecasXadrez.__dict__ if i not in special_dicts)
    return pecas


def tabuleiro_vazio():
    """
    :return: list 8x8 preenchida de False

    Usado em get_movimentos
    """

    return [[False] * 8 for _ in range(8)]


'''
Para as classes abaixo saiba que:
    * self.cor representa a cor da peça, sendo que True significa que a peça é branca e False preta
    * self.nome_cor é um atributo usado no módulo Recurso
    * self.movimentou é usado para saber se a peça se movimentou

As classe abaixo usa a seguinte interface:
    * movimento(self, tabuleiro: list 8x8, old_posicao: list, new_posicao: list) -> bool ou ações especiais 
    * get_movimentos(self, tabuleiro: list 8x8, posicao: list) -> list 8x8 de bool
'''


class Rei:
    def __init__(self, cor: bool, movimentou: bool = False):
        """
        :param cor: True é branco e False é preto
        :param movimentou: Se a peça movimentou, por padrão é False
        """

        self.nome = 'Rei'
        self.cor = cor
        self.nome_cor = '{}_{}'.format(self.nome, 'branco' if cor else 'preto')
        self.movimentou = movimentou

    def movimento(self, tabuleiro, old_posicao: tuple, new_posicao: tuple) -> bool:
        """
        :param tabuleiro: list 8x8
        :param old_posicao: (i, j)
        :param new_posicao: (i, j)
        :return: bool mostrando se o movimento de old_posicao para new_posicao é um movimento válido

        O atributo movimentou fica True
        """

        new_linha, new_coluna = new_posicao
        if self.get_movimentos(tabuleiro, old_posicao)[new_linha][new_coluna]:
            self.movimentou = True
            return True
        return False

    def get_movimentos(self, tabuleiro, posicao: tuple):  # TODO Roque
        """
        :param tabuleiro: list 8x8
        :param posicao: (i, j)
        :return: list 8x8 de valores bool que mostra todos os movimentos possíveis
        """

        res = tabuleiro_vazio()
        linha, coluna = posicao

        # Verificando as três casas acima do rei
        i = linha + 1
        if -1 < i < 8:
            j = coluna  # Meio
            if -1 < j < 8:
                # Se o Tabuleiro esta vazio ou a peça é inimiga res[i][j] recebe True
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            j = coluna + 1  # Direita
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            j = coluna - 1  # Esquerda
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

        # Verificando as três casas abaixo do rei
        i = linha - 1
        if -1 < i < 8:
            j = coluna  # Meio
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            j = coluna + 1  # Direita
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            j = coluna - 1  # Esquerda
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

        # Duas casas ao lado do rei
        j = coluna + 1  # Direita
        if -1 < j < 8:
            res[linha][j] = tabuleiro[linha][j] is None or tabuleiro[linha][j].cor != self.cor

        j = coluna - 1  # Esquerda
        if -1 < j < 8:
            res[linha][j] = tabuleiro[linha][j] is None or tabuleiro[linha][j].cor != self.cor

        return res


class Rainha:
    def __init__(self, cor: bool):
        """:param cor: True é branco e False é preto"""

        self.nome = 'Rainha'
        self.cor = cor
        self.nome_cor = '{}_{}'.format(self.nome, 'branco' if cor else 'preto')

    def movimento(self, tabuleiro, old_posicao: tuple, new_posicao: tuple) -> bool:
        """
        :param tabuleiro: list 8x8
        :param old_posicao: [i, j]
        :param new_posicao: [i, j]
        :return: bool mostrando se o movimento de old_posicao para new_posicao é um movimento válido
        """

        new_linha, new_coluna = new_posicao
        if self.get_movimentos(tabuleiro, old_posicao)[new_linha][new_coluna]:
            return True
        return False

    def get_movimentos(self, tabuleiro, posicao: tuple):
        """
        :param tabuleiro: list 8x8
        :param posicao: [i, j]
        :return: list 8x8 de valores bool que mostra todos os movimentos possíveis
        """

        linha, coluna = posicao

        res = tabuleiro_vazio()

        # Horizontal e Vertical
        for i in range(linha + 1, 8):  # Para direita
            if tabuleiro[i][coluna] is None:
                res[i][coluna] = True
            else:
                res[i][coluna] = self.cor != tabuleiro[i][coluna].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        for i in range(linha - 1, -1, -1):  # Para esquerda
            if tabuleiro[i][coluna] is None:
                res[i][coluna] = True
            else:
                res[i][coluna] = self.cor != tabuleiro[i][coluna].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        for i in range(coluna + 1, 8):  # Para cima
            if tabuleiro[linha][i] is None:
                res[linha][i] = True
            else:
                res[linha][i] = self.cor != tabuleiro[linha][i].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        for i in range(coluna - 1, -1, -1):  # Para baixo
            if tabuleiro[linha][i] is None:
                res[linha][i] = True
            else:
                res[linha][i] = self.cor != tabuleiro[linha][i].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        # Diagonais
        i, j = posicao
        while i < 7 and j < 7:  # Diagonal direita pra cima
            i += 1
            j += 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        i, j = posicao
        while i > 0 and j < 7:  # Diagonal direita baixo
            i -= 1
            j += 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        i, j = posicao
        while i < 7 and j > 0:  # Diagonal esquerda cima
            i += 1
            j -= 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        i, j = posicao
        while i > 0 and j > 0:  # Diagonal esquerda baixo
            i -= 1
            j -= 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        return res


class Bispo:
    def __init__(self, cor: bool):
        """:param cor: True é branco e False é preto"""

        self.nome = 'Bispo'
        self.cor = cor
        self.nome_cor = '{}_{}'.format(self.nome, 'branco' if cor else 'preto')

    def movimento(self, tabuleiro, old_posicao: tuple, new_posicao: tuple) -> bool:
        """
        :param tabuleiro: list 8x8
        :param old_posicao: (i, j)
        :param new_posicao: (i, j)
        :return: bool mostrando se o movimento de old_posicao para new_posicao é um movimento válido
        """

        new_linha, new_coluna = new_posicao
        if self.get_movimentos(tabuleiro, old_posicao)[new_linha][new_coluna]:
            return True
        return False

    def get_movimentos(self, tabuleiro, posicao: tuple):
        """
        :param tabuleiro: list 8x8
        :param posicao: (i, j)
        :return: list 8x8 de valores bool que mostra todos os movimentos possíveis
        """

        res = tabuleiro_vazio()

        i, j = posicao
        while i < 7 and j < 7:  # Diagonal direita pra cima
            i += 1
            j += 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        i, j = posicao
        while i > 0 and j < 7:  # Diagonal direita baixo
            i -= 1
            j += 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        i, j = posicao
        while i < 7 and j > 0:  # Diagonal esquerda cima
            i += 1
            j -= 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        i, j = posicao
        while i > 0 and j > 0:  # Diagonal esquerda baixo
            i -= 1
            j -= 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        return res


class Cavalo:
    def __init__(self, cor: bool):
        """:param cor: True é branco e False é preto"""

        self.nome = 'Cavalo'
        self.cor = cor
        self.nome_cor = '{}_{}'.format(self.nome, 'branco' if cor else 'preto')

    def movimento(self, tabuleiro, old_posicao: tuple, new_posicao: tuple) -> bool:
        """
        :param tabuleiro: list 8x8
        :param old_posicao: (i, j)
        :param new_posicao: (i, j)
        :return: bool mostrando se o movimento de old_posicao para new_posicao é um movimento válido
        """

        new_linha, new_coluna = new_posicao
        if self.get_movimentos(tabuleiro, old_posicao)[new_linha][new_coluna]:
            return True
        return False

    def get_movimentos(self, tabuleiro, posicao: tuple):
        """
        :param tabuleiro: list 8x8
        :param posicao: (i, j)
        :return: list 8x8 de valores bool que mostra todos os movimentos possíveis
        """

        res = tabuleiro_vazio()
        linha, coluna = posicao

        i = linha + 2  # Cima
        if -1 < i < 8:
            j = coluna + 1  # Cima cima direita
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            j = coluna - 1
            if -1 < j < 8:  # Cima cima esquerda
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

        j = coluna + 2  # Direita
        if -1 < j < 8:
            i = linha + 1  # Direita direita cima
            if -1 < i < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            i = linha - 1
            if -1 < i < 8:  # Direita direita baixo
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

        i = linha - 2  # Baixo
        if -1 < i < 8:
            j = coluna + 1  # Baixo baixo direita
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            j = coluna - 1  # Baixo baixo esquerda
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

        # Esquerda
        j = coluna - 2
        if -1 < j < 8:
            i = linha + 1  # Esquerda esquerda cima
            if -1 < i < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            i = linha - 1  # Esquerda esquerda cima
            if -1 < i < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

        return res


class Torre:
    def __init__(self, cor, movimentou: bool = False):
        """
        :param cor: True é branco e False é preto
        :param movimentou: Se a peça movimentou, por padrão é False
        """

        self.nome = 'Torre'
        self.cor = cor
        self.nome_cor = '{}_{}'.format(self.nome, 'branco' if cor else 'preto')
        self.movimentou = movimentou

    def movimento(self, tabuleiro, old_posicao: tuple, new_posicao: tuple) -> bool:
        """
        :param tabuleiro: list 8x8
        :param old_posicao: (i, j)
        :param new_posicao: (i, j)
        :return: bool mostrando se o movimento de old_posicao para new_posicao é um movimento válido

        O atributo movimentou fica True
        """

        new_linha, new_coluna = new_posicao
        if self.get_movimentos(tabuleiro, old_posicao)[new_linha][new_coluna]:
            self.movimentou = True
            return True
        return False

    def get_movimentos(self, tabuleiro, posicao: tuple):
        """
        :param tabuleiro: list 8x8
        :param posicao: (i, j)
        :return: list 8x8 de valores bool que mostra todos os movimentos possíveis
        """

        linha, coluna = posicao

        res = tabuleiro_vazio()
        for i in range(linha + 1, 8):  # Para direita
            if tabuleiro[i][coluna] is None:
                res[i][coluna] = True
            else:
                res[i][coluna] = self.cor != tabuleiro[i][coluna].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        for i in range(linha - 1, -1, -1):  # Para esquerda
            if tabuleiro[i][coluna] is None:
                res[i][coluna] = True
            else:
                res[i][coluna] = self.cor != tabuleiro[i][coluna].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        for i in range(coluna + 1, 8):  # Para cima
            if tabuleiro[linha][i] is None:
                res[linha][i] = True
            else:
                res[linha][i] = self.cor != tabuleiro[linha][i].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        for i in range(coluna - 1, -1, -1):  # Para baixo
            if tabuleiro[linha][i] is None:
                res[linha][i] = True
            else:
                res[linha][i] = self.cor != tabuleiro[linha][i].cor
                break  # Casa não esta vazia, não há porquê verificar as casas seguintes

        return res


class Peao:
    enpassant = property()

    @enpassant.getter
    def enpassant(self) -> tuple:
        return self.__enpassant

    # posicao = [linha, coluna]
    # Retorna [posicao inicial, posicao por que passou, posicao final]
    @enpassant.setter
    def enpassant(self, value: tuple):
        """
        :param value: (old_posicao, new_posicao), ou seja ((i, j),(i, j))

        O atributo enpassant vira um list com os seguinte formato:
[posicao inicial, posicao por que passou, posicao final]
        Ou ser None se o valor é invalido
        Observação: não verifica se a peça inimiga é realmente um Peao
        """

        if value:
            d = 1 if self.cor else -1  # Define a direção que esse Peao anda
            old_posicao, new_posicao = value
            print(f'new_posicao == {new_posicao[0]}')
            if old_posicao[0] == new_posicao[0] + 2 * d:  # Se o Peao tiver pulado duas casas # FIXME
                print(f'new == {new_posicao[0]} e old = {old_posicao[0]}')
                i, j = new_posicao[0] + d, new_posicao[1]  # Calcula posição pelo qual o Peao passou
                self.__enpassant = old_posicao, (i, j), new_posicao
            else:  # Se o Peao não tiver pulado duas casas
                self.__enpassant = None
        else:  # Se atribuir o valor None a enpassant
            self.__enpassant = None

    def __init__(self, cor: bool, movimentou: bool = False):
        """
        :param cor: True é branco e False é preto
        :param movimentou: Se a peça movimentou, por padrão é False
        """

        self.nome = 'Peao'
        self.cor = cor
        self.nome_cor = '{}_{}'.format(self.nome, 'branco' if cor else 'preto')  # Usado no módulo Recurso
        self.__enpassant = None  # Valor property enpassant
        self.movimentou = movimentou

    def movimento(self, tabuleiro, old_posicao: tuple, new_posicao: tuple):
        """
        :param tabuleiro: list 8x8
        :param old_posicao: (i, j)
        :param new_posicao: (i, j)
        :return: bool mostrando se o movimento de old_posicao para new_posicao é um movimento válido
        :return: Se for um movimento especial retorne uma tupla no seguinte formato: (movimento, posicao: tuple)

        O atributo movimentou fica True
        """

        new_linha, new_coluna = new_posicao
        movimentos = self.get_movimentos(tabuleiro, old_posicao)[new_linha][new_coluna]
        if movimentos:
            self.movimentou = True

            # Promoção
            promocao = 7 if self.cor else 0  # Se a cor for branca a posição para ter a promoção é 7 senão é 0
            if new_linha == promocao:
                return 'promocao', new_posicao  # O movimento é promocao

            # Movimento Enpassat
            elif self.enpassant and new_posicao == self.enpassant[1]:
                res = 'enpassant', self.enpassant[2]
                self.enpassant = None
                return res  # O movimento é enpassant

            return True  # O movimento é possivel

        return False  # O movimento impossivel

    def get_movimentos(self, tabuleiro, posicao: tuple):
        """
        :param tabuleiro: list 8x8
        :param posicao: (i, j)
        :return: list 8x8 de valores bool que mostra todos os movimentos possíveis
        """

        linha, coluna = posicao

        res = tabuleiro_vazio()
        d = 1 if self.cor else -1  # Define a direção que o Peao anda
        i = linha + d

        # Movimento normal
        if -1 < linha + d < 8:
            ultimo = res[i][coluna] = tabuleiro[i][coluna] is None

            # Capturas
            j = coluna + 1  # Diagonal direita
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is not None and self.cor != tabuleiro[i][j].cor

            j = coluna - 1  # Diagonl esquerda
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is not None and self.cor != tabuleiro[i][j].cor

            # Movimento especial de andar por duas casas
            i = linha + d * 2
            if -1 < i < 8 and not self.movimentou and ultimo:
                res[i][coluna] = tabuleiro[i][coluna] is None

        # Movimento en passant
        if self.enpassant:
            new_linha, new_coluna = self.enpassant[2]

            # Se a peça for um Peao
            if isinstance(tabuleiro[new_linha][new_coluna], Peao):
                # Se os Peaos estiverem um do lado do outro
                if new_linha == linha and (new_coluna == coluna + 1 or new_coluna == coluna - 1):
                    pas_linha, pas_coluna = self.enpassant[1]  # Posicao por onde o Peao inimigo Passou
                    print("enpassant é possivel")
                    res[pas_linha][pas_coluna] = True  # A casa que o Peao inimigo passou recebe True

        return res
