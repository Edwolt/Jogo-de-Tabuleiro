def game(game_name):
    if game_name == 'xadrez':
        from Views.ViewXadrez import Tela
        tela = Tela(800, pacote_cor='Marrom2')
        tela.novo_jogo()
    else:
        raise Exception('Modo de jogo não encontrado')
