def nome_pecas():
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
    pecas = [i for i in PecasXadrez.__dict__ if i not in special_dicts]
    return pecas


def tabuleiro_vazio():
    return [[False] * 8 for _ in range(8)]


class Rei:
    def __init__(self, cor, movimentou=False):
        self.nome = 'Rei'
        self.cor = cor
        self.nome_cor = '{}_{}'.format(self.nome, 'branco' if cor else 'preto')
        self.movimentou = movimentou

    def movimento(self, tabuleiro, old_posicao, new_posicao):
        new_linha, new_coluna = new_posicao
        if self.get_movimentos(tabuleiro, old_posicao)[new_linha][new_coluna]:
            self.movimentou = True
            return True
        return False

    def get_movimentos(self, tabuleiro, posicao):
        res = tabuleiro_vazio()
        linha, coluna = posicao

        # Três casas acima do rei
        i = linha + 1
        if -1 < i < 8:
            j = coluna
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            j = coluna + 1
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            j = coluna - 1
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

        # Três casas abaixo do rei
        i = linha - 1
        if -1 < i < 8:
            j = coluna
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            j = coluna + 1
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            j = coluna - 1
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

        # Duas casas ao lado do rei
        j = coluna + 1
        if -1 < j < 8:
            res[linha][j] = tabuleiro[linha][j] is None or tabuleiro[linha][j].cor != self.cor

        j = coluna - 1
        if -1 < j < 8:
            res[linha][j] = tabuleiro[linha][j] is None or tabuleiro[linha][j].cor != self.cor

        return res


class Rainha:
    def __init__(self, cor):
        self.nome = 'Rainha'
        self.cor = cor
        self.nome_cor = '{}_{}'.format(self.nome, 'branco' if cor else 'preto')

    def movimento(self, tabuleiro, old_posicao, new_posicao):
        new_linha, new_coluna = new_posicao
        if self.get_movimentos(tabuleiro, old_posicao)[new_linha][new_coluna]:
            return True
        return False

    def get_movimentos(self, tabuleiro, posicao):
        linha, coluna = posicao

        res = tabuleiro_vazio()

        # Horizontal e Vertical
        for i in range(linha + 1, 8):
            if tabuleiro[i][coluna] is None:
                res[i][coluna] = True
            else:
                res[i][coluna] = self.cor != tabuleiro[i][coluna].cor
                break

        for i in range(linha - 1, -1, -1):
            if tabuleiro[i][coluna] is None:
                res[i][coluna] = True
            else:
                res[i][coluna] = self.cor != tabuleiro[i][coluna].cor
                break

        for i in range(coluna + 1, 8):
            if tabuleiro[linha][i] is None:
                res[linha][i] = True
            else:
                res[linha][i] = self.cor != tabuleiro[linha][i].cor
                break

        for i in range(coluna - 1, -1, -1):
            if tabuleiro[linha][i] is None:
                res[linha][i] = True
            else:
                res[linha][i] = self.cor != tabuleiro[linha][i].cor
                break

        # Diagonais
        i, j = posicao
        while i < 7 and j < 7:
            i += 1
            j += 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break

        i, j = posicao
        while i > 0 and j < 7:
            i -= 1
            j += 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break

        i, j = posicao
        while i < 7 and j > 0:
            i += 1
            j -= 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break

        i, j = posicao
        while i > 0 and j > 0:
            i -= 1
            j -= 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break

        return res


class Bispo:
    def __init__(self, cor):
        self.nome = 'Bispo'
        self.cor = cor
        self.nome_cor = '{}_{}'.format(self.nome, 'branco' if cor else 'preto')

    def movimento(self, tabuleiro, old_posicao, new_posicao):
        new_linha, new_coluna = new_posicao
        if self.get_movimentos(tabuleiro, old_posicao)[new_linha][new_coluna]:
            return True
        return False

    def get_movimentos(self, tabuleiro, posicao):
        res = tabuleiro_vazio()

        i, j = posicao
        while i < 7 and j < 7:
            i += 1
            j += 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break

        i, j = posicao
        while i > 0 and j < 7:
            i -= 1
            j += 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break

        i, j = posicao
        while i < 7 and j > 0:
            i += 1
            j -= 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break

        i, j = posicao
        while i > 0 and j > 0:
            i -= 1
            j -= 1
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = self.cor != tabuleiro[i][j].cor
                break

        return res


class Cavalo:
    def __init__(self, cor):
        self.nome = 'Cavalo'
        self.cor = cor
        self.nome_cor = '{}_{}'.format(self.nome, 'branco' if cor else 'preto')

    def movimento(self, tabuleiro, old_posicao, new_posicao):
        new_linha, new_coluna = new_posicao
        if self.get_movimentos(tabuleiro, old_posicao)[new_linha][new_coluna]:
            return True
        return False

    def get_movimentos(self, tabuleiro, posicao):
        res = tabuleiro_vazio()
        linha, coluna = posicao

        # Cima
        i = linha + 2
        if -1 < i < 8:
            j = coluna + 1
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            j = coluna - 1
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

        # Direita
        j = coluna + 2
        if -1 < j < 8:
            i = linha + 1
            if -1 < i < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            i = linha - 1
            if -1 < i < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

        # Baixo
        i = linha - 2
        if -1 < i < 8:
            j = coluna + 1
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            j = coluna - 1
            if -1 < j < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

        # Esquerda
        j = coluna - 2
        if -1 < j < 8:
            i = linha + 1
            if -1 < i < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

            i = linha - 1
            if -1 < i < 8:
                res[i][j] = tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

        return res


class Torre:
    def __init__(self, cor, movimentou=False):
        self.nome = 'Torre'
        self.cor = cor
        self.nome_cor = '{}_{}'.format(self.nome, 'branco' if cor else 'preto')
        self.movimentou = movimentou

    def movimento(self, tabuleiro, old_posicao, new_posicao):
        new_linha, new_coluna = new_posicao
        if self.get_movimentos(tabuleiro, old_posicao)[new_linha][new_coluna]:
            self.movimentou = True
            return True
        return False

    def get_movimentos(self, tabuleiro, posicao):
        linha, coluna = posicao

        res = tabuleiro_vazio()
        for i in range(linha + 1, 8):
            if tabuleiro[i][coluna] is None:
                res[i][coluna] = True
            else:
                res[i][coluna] = self.cor != tabuleiro[i][coluna].cor
                break

        for i in range(linha - 1, -1, -1):
            if tabuleiro[i][coluna] is None:
                res[i][coluna] = True
            else:
                res[i][coluna] = self.cor != tabuleiro[i][coluna].cor
                break

        for i in range(coluna + 1, 8):
            if tabuleiro[linha][i] is None:
                res[linha][i] = True
            else:
                res[linha][i] = self.cor != tabuleiro[linha][i].cor
                break

        for i in range(coluna - 1, -1, -1):
            if tabuleiro[linha][i] is None:
                res[linha][i] = True
            else:
                res[linha][i] = self.cor != tabuleiro[linha][i].cor
                break

        return res


class Peao:
    enpassant = property()

    @enpassant.getter
    def enpassant(self):
        return self.__enpassant

    # posicao = [linha, coluna]
    # Retorna [posicao inicial, posicao por que passou, posicao final]
    @enpassant.setter
    def enpassant(self, value):
        if value:
            d = 1 if self.cor else -1
            old_posicao, new_posicao = value
            if old_posicao[0] == new_posicao[0] + 2 * d:  # Se o Peao tiver pulado duas casas
                i, j = new_posicao[0] + d, new_posicao[1]
                self.__enpassant = [old_posicao, [i, j], new_posicao]
            else:  # Se o Peao não tiver pulado duas casas
                self.__enpassant = None
        else:  # Se atribuir um valor nulo (tipo None)
            self.__enpassant = None

    def __init__(self, cor, movimentou=False):
        self.nome = 'Peao'
        self.cor = cor
        self.nome_cor = '{}_{}'.format(self.nome, 'branco' if cor else 'preto')
        self.__enpassant = None
        self.movimentou = movimentou

    def movimento(self, tabuleiro, old_posicao, new_posicao):
        new_linha, new_coluna = new_posicao
        movimentos = self.get_movimentos(tabuleiro, old_posicao)[new_linha][new_coluna]
        if movimentos:
            self.movimentou = True

            # Promoção
            promocao = 7 if self.cor else 0
            if new_linha == promocao:
                return 'promocao', new_posicao

            # Movimento Enpassat
            elif self.enpassant and new_posicao == self.enpassant[1]:
                res = 'enpassant', self.enpassant[2]
                self.enpassant = None
                return res

            # Movimento Possivel
            return True
        # Movimento impossivel
        return False

    def get_movimentos(self, tabuleiro, posicao):
        linha, coluna = posicao

        res = tabuleiro_vazio()
        d = 1 if self.cor else -1
        i = linha + d

        # Movimento Normal
        if 0 <= linha + d < 8:
            ultimo = res[i][coluna] = tabuleiro[i][coluna] is None

            # Capturas
            j = coluna + 1
            if 0 <= j < 8:
                res[i][j] = tabuleiro[i][j] is not None and self.cor != tabuleiro[i][j].cor

            j = coluna - 1
            if 0 <= j < 8:
                res[i][j] = tabuleiro[i][j] is not None and self.cor != tabuleiro[i][j].cor

            # Movimento Especial de andar por duas casas
            i = linha + d * 2
            if 0 <= i < 8 and not self.movimentou and ultimo:
                res[i][coluna] = tabuleiro[i][coluna] is None

        # Movimento en passant
        if self.enpassant:
            new_linha, new_coluna = self.enpassant[2]

            # Se a peca for um Peao
            if isinstance(tabuleiro[new_linha][new_coluna], Peao):
                # Se os Peaos estiverem um do lado do outro
                if new_linha == linha and (new_coluna == coluna + 1 or new_coluna == coluna - 1):
                    pas_linha, pas_coluna = self.enpassant[1]
                    res[pas_linha][pas_coluna] = True

        return res
