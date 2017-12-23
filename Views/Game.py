def game(game_name):
    if game_name == 'xadrez':
        from Views.ViewXadrez import Tela
        tela = Tela(800)
        a = 'marrom'
        if a == 'marrom':
            tela = Tela(800, pacote_cor='marrom')
            # tela.set_cores([214, 165, 132], [124, 49, 0])
        if a == 'marrom2':
            tela.set_cores(
                [214, 165, 132],
                [124, 49, 0],
                [153, 0, 0],
                [229, 126, 0]
            )
        if a == 'marrom2':
            tela.set_cores(
                [214, 165, 132],
                [124, 49, 0],
                [153, 0, 0],
                [229, 126, 0]
            )
        if a == 'azul':
            tela.set_cores([94, 255, 91], [0, 14, 173])
        if a == 'random':
            from random import randint as random
            tela.del_cores()
            tela.set_cores(
                [random(0, 255), random(0, 255), random(0, 255)],
                [random(0, 255), random(0, 255), random(0, 255)],
                [random(0, 255), random(0, 255), random(0, 255)],
                [random(0, 255), random(0, 255), random(0, 255)]
            )
        if a == 'random2':
            from random import randint as random
            tela.del_cores()
            tela.set_cores(
                branco=[random(0, 255), random(0, 255), random(0, 255)],
                preto=[random(0, 255), random(0, 255), random(0, 255)],
                click=[random(0, 255), random(0, 255), random(0, 255)],
                movimentopreto=[random(0, 255), random(0, 255), random(0, 255)],
                movimentobranco=[random(0, 255), random(0, 255), random(0, 255)]
            )
            tela.set_config(movimento=lambda cores, i, j: \
                cores['movimentopreto'] if (i + j) % 2 else cores['movimentobranco'])
        if a == 'random3':
            from random import randint as random
            tela.del_cores()
            tela.set_cores(
                cor1=[random(0, 255), random(0, 255), random(0, 255)],
                cor2=[random(0, 255), random(0, 255), random(0, 255)],
                cor3=[random(0, 255), random(0, 255), random(0, 255)],
                click=[random(0, 255), random(0, 255), random(0, 255)],
                movimentopreto=[random(0, 255), random(0, 255), random(0, 255)],
                movimentobranco=[random(0, 255), random(0, 255), random(0, 255)]
            )
            b = lambda cores, i, j: \
                cores['movimentopreto'] if (i + j) % 2 else cores['movimentobranco']

            def quad(cores, i, j):
                if (i + j) % 3 == 0:
                    return cores['cor1']
                elif (i + j) % 3 == 1:
                    return cores['cor2']
                elif (i + j) % 3 == 2:
                    return cores['cor3']

            tela.set_config(movimento=b, quadrado=quad)

        tela.novo_jogo()




    else:
        raise Exception('Modo de jogo não encontrado')
