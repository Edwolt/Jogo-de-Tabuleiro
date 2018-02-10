"""Inicie o Jogo"""

JOGO = 'Xadrez'  # Nome do jogo a ser jogado

JOGO = JOGO.lower()
if JOGO == 'xadrez':
    from Views.ViewXadrez import Tela

    tela = Tela(800)
    tela.novo_jogo()
else:
    raise Exception('Modo de jogo não encontrado')
