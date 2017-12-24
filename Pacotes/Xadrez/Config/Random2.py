from random import randint as random

del_cores = True

cores = {
    'branco': [random(0, 255), random(0, 255), random(0, 255)],
    'preto': [random(0, 255), random(0, 255), random(0, 255)],
    'click': [random(0, 255), random(0, 255), random(0, 255)],
    'movimentopreto': [random(0, 255), random(0, 255), random(0, 255)],
    'movimentobranco': [random(0, 255), random(0, 255), random(0, 255)]
}

config = {
    'movimento': lambda cor, i, j: cor['movimentopreto'] if (i + j) % 2 else cor['movimentobranco']
}
