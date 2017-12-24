from random import randint as random

del_cores = True

cores = {
    'branco': [random(0, 255), random(0, 255), random(0, 255)],
    'preto': [random(0, 255), random(0, 255), random(0, 255)],
    'click0': [random(0, 255), random(0, 255), random(0, 255)],
    'click1': [random(0, 255), random(0, 255), random(0, 255)],
    'movimento0': [random(0, 255), random(0, 255), random(0, 255)],
    'movimento1': [random(0, 255), random(0, 255), random(0, 255)],
    'captura0': [random(0, 255), random(0, 255), random(0, 255)],
    'captura1': [random(0, 255), random(0, 255), random(0, 255)]
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
    'captur': lambda cor, i, j: cor['captura0'] if (i + j) % 2 else cor['captura1'],
    'titulo': lambda vez: x + ' : ' + (p1 if vez else p2)
}
