from random import randint as random

del_cores = True

cores = {
    'cor1': [random(0, 255), random(0, 255), random(0, 255)],
    'cor2': [random(0, 255), random(0, 255), random(0, 255)],
    'cor3': [random(0, 255), random(0, 255), random(0, 255)],
    'click': [random(0, 255), random(0, 255), random(0, 255)],
    'movimentopreto': [random(0, 255), random(0, 255), random(0, 255)],
    'movimentobranco': [random(0, 255), random(0, 255), random(0, 255)]
}


def quad(cores, i, j):
    if (i + j) % 3 == 0:
        return cores['cor1']
    elif (i + j) % 3 == 1:
        return cores['cor2']
    elif (i + j) % 3 == 2:
        return cores['cor3']


config = {
    'movimento': lambda cor, i, j: cor['movimentopreto'] if (i + j) % 2 else cor['movimentobranco'],
    'quadrado': quad
}
