__author__ = 'Eduardo Souza Rocha'

from random import randint as random

del_cores = True


def cor():
    return random(0, 255), random(0, 255), random(0, 255)


def nome(vez):
    x, p1, p2 = nomes[random(0, len(nomes) - 1)]
    return x + ' : ' + (p1 if vez else p2)


cores = dict()

nomes = (
    ('Xadrez', 'Branco', 'Preto'),
    ('Jogo de Tabuleiro', 'Claro', 'Escuro'),
    ('Chess', 'Black', 'White'),
    ('Chess Game', 'Player 1', 'Player 2'),
)
config = {
    'quadrado': lambda c, i, j: cor(),
    'click': lambda c, i, j: cor(),
    'movimento': lambda c, i, j: cor(),
    'captura': lambda c, i, j: cor(),
    'titulo': lambda vez: nome(vez),
    'menu': lambda c, menu: cor(),
    'cor_fonte': lambda c, menu: cor()
}
