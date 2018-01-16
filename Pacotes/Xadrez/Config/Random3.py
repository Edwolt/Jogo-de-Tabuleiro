from random import randint as random

del_cores = True


def gerar_cor():
    return [random(0, 255), random(0, 255), random(0, 255)]


def to_str(iterable):
    res = ''
    for i in iterable:
        res += i
    return res


cores = {
    'cor1': gerar_cor(),
    'cor2': gerar_cor(),
    'cor3': gerar_cor(),
    'click': gerar_cor(),
    'movimentopreto': gerar_cor(),
    'movimentobranco': gerar_cor(),
    'Menu': gerar_cor(),
    'MenuConfigs': gerar_cor(),
    'MenuImagens': gerar_cor(),
    'MenuFontes': gerar_cor(),
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
    'quadrado': quad,
    'menu': lambda cor, menu: cor[to_str(menu)],
    'cor_fonte': lambda cor, menu: cor['MenuFontes']
}
