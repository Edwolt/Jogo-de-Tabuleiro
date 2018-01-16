from random import randint as random

del_cores = True


def cor():
    return [random(0, 255), random(0, 255), random(0, 255)]


def to_str(iterable):
    res = ''
    for i in iterable:
        res += i
    return res


cores = {
    'branco': cor(),
    'preto': cor(),
    'click0': cor(),
    'click1': cor(),
    'movimento0': cor(),
    'movimento1': cor(),
    'captura0': cor(),
    'captura1': cor(),
    'Menu': cor(),
    'MenuConfigs': cor(),
    'MenuImagens': cor(),
    'MenuFontes': cor(),
    'FonteMenu': cor(),
    'FonteMenuConfigs': cor(),
    'FonteMenuImagens': cor(),
    'FonteMenuFontes': cor()
}

nomes = (
    ('Xadrez', 'Branco', 'Preto'),
    ('Jogo de Tabuleiro', 'Claro', 'Escuro'),
    ('Chess', 'Black', 'White'),
    ('Chess Game', 'Player 1', 'Player 2'),
)

x, p1, p2 = t = nomes[random(0, len(nomes) - 1)]
config = {
    'movimento': lambda cor, i, j: cor['movimento0'] if (i + j) % 2 else cor['movimento1'],
    'click': lambda cor, i, j: cor['click0'] if (i + j) % 2 else cor['click1'],
    'captura': lambda cor, i, j: cor['captura0'] if (i + j) % 2 else cor['captura1'],
    'titulo': lambda vez: x + ' : ' + (p1 if vez else p2),
    'menu': lambda cor, menu: cor[to_str(menu)],
    'cor_fonte': lambda cor, menu: cor['Fonte' + to_str(menu)]
}
