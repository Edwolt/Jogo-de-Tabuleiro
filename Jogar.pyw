GAME = 'Xadrez'

GAME = GAME.lower()
if GAME == 'xadrez':
    from Views.ViewXadrez import Tela

    tela = Tela(800, pacote_config='Random')
    tela.novo_jogo()
else:
    raise Exception('Modo de jogo não encontrado')
