def game(game_name):
    if game_name == 'xadrez':
        from Views.ViewXadrez import Tela
        tela = Tela(800)
        # tela.set_cores([94, 255, 91], [0, 14, 173])
        tela.set_config([214, 165, 132], [124, 49, 0])
        from random import randint as random
        tela.del_config()
        tela.set_config(
            [random(0, 255), random(0, 255), random(0, 255)],
            [random(0, 255), random(0, 255), random(0, 255)],
            [random(0, 255), random(0, 255), random(0, 255)],
            movimentopreto=[random(0, 255), random(0, 255), random(0, 255)],
            movimentobranco=[random(0, 255), random(0, 255), random(0, 255)]
        )
        tela.config['movimento'] = lambda cores, i, j: \
            cores['movimentopreto'] if (i + j) % 2 else cores['movimentobranco']
        tela.novo_jogo()
    else:
        raise Exception('Modo de jogo não encontrado')
