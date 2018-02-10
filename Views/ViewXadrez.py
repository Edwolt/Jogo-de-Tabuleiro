import pygame

from Class.Recursos import Recursos
from Class.Xadrez import Xadrez


class Tela:
    """Exibe o Jogo de Xadrez"""
    pacote_img = property()

    @pacote_img.setter
    def pacote_img(self, value):
        self.recursos.pacote = value

    pacote_config = property()

    @pacote_config.setter
    def pacote_config(self, value):
        """
        :param value: Uma str com o nome da config, se for None os valores ficam padrão
        """

        # Configs para o padrão, pois independente de value esse passo será necessário
        self.config = {
            'quadrado': lambda cores, i, j: cores['branco'] if (i + j) % 2 == 0 else self.cores['preto'],
            'click': lambda cores, i, j: cores['click'],
            'movimento': lambda cores, i, j: cores['movimento'],
            'captura': lambda cores, i, j: self.config['movimento'](cores, i, j),
            'titulo': lambda vez: 'Xadrez : ' + ('Branco' if vez else 'Preto'),
            'menu': lambda cores, menu: self.cores['menu'],
            'cor_fonte': lambda cores, menu: self.cores['cor_fonte']
        }
        if value is not None:
            self.recursos.config = value  # Atribui ao recursos.config o value para ter acesso ao modulo

            if self.recursos.config.del_cores:
                # Deleta cores
                self.del_cores()
            else:
                # Cores padrões
                self.set_cores(
                    branco=(255, 255, 255),
                    preto=(0, 0, 0),
                    click=(255, 0, 0),
                    movimento=(0, 255, 255),
                    menu=(0, 0, 0),
                    cor_fonte=(255, 255, 255)
                )

            if self.recursos.config.cores:
                self.set_cores(**self.recursos.config.cores)

            if self.recursos.config.config:
                self.set_config(**self.recursos.config.config)
        else:
            # Define as cores para o padrão, as configs já estão padrão
            self.del_cores()
            self.set_cores(
                branco=(255, 255, 255),
                preto=(0, 0, 0),
                click=(255, 0, 0),
                movimento=(0, 255, 255),
                menu=(0, 0, 0),
                cor_fonte=(255, 255, 255)
            )

    fonte = property()

    @fonte.setter
    def fonte(self, value):
        self.__config['fonte'] = pygame.font.Font(f'Pacotes/Xadrez/Fontes/{value}', 50)

    def __init__(self, size: int = 800, framerate: int = 60, pacote_config: str = None):
        """
        :param size: O tamanho do jogo
        :param framerate: Quantas vezes o jogos
        :param pacote_config: Pacote de config que será utilizado
        """

        pygame.init()  # Inicio do Pygame
        self.screen = pygame.display.set_mode((size, size))  # Mostrando tela # TODO permitir mudar tamanho da tela

        self.xadrez = Xadrez()  # Aqui está tudo sobre o jogo
        self.recursos = Recursos('Xadrez', config=pacote_config)  # Aqui esta todas as imagens e configs
        self.__clock = pygame.time.Clock()  # Relógio para seguir o framerate

        self.tabuleiro = None
        self.__click = 0, 0  # Onde foi o último click, inicia com 0, 0
        self.framerate = framerate
        self.quad_size = size / 8  # Tamanho de cada quadrado a ser exibido
        self.cores = dict()
        self.config = dict()
        self.pacote_config = pacote_config  # Usa os valores de config especificados, se for não é escolhido o padrão

        # Cria uma Surface para ser usado como as casas do tabuleiro
        self.quad = lambda: pygame.Surface((self.quad_size, self.quad_size))
        # Cria um retangulo para ser usado em imagens
        self.rect = lambda: pygame.Rect((0, 0), (self.quad_size, self.quad_size))

        # Com esse atributo que são acessadas as configs
        self.__config = {
            'quadrado': lambda i, j: self.config['quadrado'](self.cores, i, j),
            'click': lambda i, j: self.config['click'](self.cores, i, j),
            'movimento': lambda i, j: self.config['movimento'](self.cores, i, j),
            'captura': lambda i, j: self.config['captura'](self.cores, i, j),
            'titulo': lambda: self.config['titulo'](self.xadrez.vez),
            'fonte': pygame.font.Font('Pacotes/Xadrez/Fontes/Consola.ttf', 50),
            'menu': lambda menu: self.config['menu'](self.cores, menu),
            'cor_fonte': lambda menu: self.config['cor_fonte'](self.cores, menu)
        }

    def novo_jogo(self):
        """Crie um novo jogo e exiba as pecas"""

        self.xadrez.reposicionar_pecas()
        self.tabuleiro = self.criar_tabuleiro()
        self.__click = 0, 0
        self.blit_all()

        self.main()  # Entra no main loop

    def main(self):
        """execute um loop onde os eventos são verificados"""

        while True:
            self.eventos()  # Verificação de eventos
            self.__clock.tick(self.framerate)  # Adequação ao framerates

    def eventos(self):
        """Verifique todos os Eventos"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Clicou no botão fechar
                quit(0)

            if event.type == pygame.KEYDOWN:  # Se alguma tecla tiver sido pressionada
                if event.key == pygame.K_ESCAPE:  # Se a tecla pressionada for o Esc
                    self.menu()  # O menu é exibido

            if event.type == pygame.MOUSEBUTTONDOWN:  # Se houve um click do botão
                self.__on_click(event)  # o metodo que verifica o clique é acionado

            if event.type == pygame.VIDEORESIZE:  # TODO permitir mudar o tamanho da tela
                pass

    def menu(self):
        """Exiba o menu"""

        from Class.Recursos import all_configs, all_imagens

        # Opçõe a ser exibidas, usado em escrever_opcoes
        opcoes = [
            'Configs',
            'Imagens',
            'Fontes',
            'Desfazer',
            'Voltar',
            'Sair'
        ]

        desfazer = 0  # Usado na opção Desfazer para saber quantas jogadas deve ser voltadas
        limite_desfazer = len(self.xadrez.jogadas)  # Quantidade máxima de jogadas que podem ser desfeitas
        selecionado = 0  # Índice da opção selecionada, utilizada em escrever_opcoes (normal, 1 e 2)
        menus = ['Menu']  # Menus abertos, exemplo: Menu1 > Menu2 > Menu3, usado em escrever_opcoes (normal, 1 e 2)
        _, height = self.__config['fonte'].size('')  # Altura que a fonte tem

        def escrever_opcoes():
            """Exiba as opções da variavel opcoes"""

            self.screen.fill(self.__config['menu'](menus))  # Pinta a tela
            y = 0  # Espaço já utilizada

            # TODO poderia exibir o menus assim Menu1 > Menu2 > Menu3
            for nivel, i in enumerate(menus):  # Passa por todas os menus abertos exibindo-os
                # Renderiza texto a ser exibido
                texto = self.__config['fonte'].render('  ' * nivel + i, 0, self.__config['cor_fonte'](menus))
                self.screen.blit(texto, [0, y])  # Exibe o texto
                y += height  # Faz com que y fique abaixo do últmo item escrito

            for i, opcao in enumerate(opcoes):
                if i == selecionado:  # Se a opção tiver sido selecionada
                    texto = '  ' * nivel + '> ' + opcao
                else:
                    texto = '  ' * nivel + '  ' + opcao

                if opcao == 'Desfazer':
                    if 0 < desfazer < limite_desfazer:  # Se desfazer não for abaixo de 0 e nem extrapolar o limite
                        texto += f' <{desfazer}>'  # Deve se mostra desfazer
                    else:  # Senão a pessoa quer começar outro jogo
                        texto = '  ' * nivel + ('> ' if opcoes[selecionado] == opcao else '  ') + 'Novo Jogo'

                # Renderiza o Texto a ser Exibido
                reder_texto = self.__config['fonte'].render(texto, 0, self.__config['cor_fonte'](menus))
                self.screen.blit(reder_texto, [0, y])  # Exibe o texto
                y += height  # Faz com que y fique abaixo do últmo item escrito

            pygame.display.flip()

        def escrever_opcoes1(opcoes: list):
            """
            Exiba as opções de um list

            :param opcoes: Opções a ser mostradas
            """

            self.screen.fill(self.__config['menu'](menus))  # Pinta a tela
            y = 0  # Espaço já utilizada

            # TODO poderia exibir o menus assim Menu1 > Menu2 > Menu3
            for nivel, i in enumerate(menus):  # Passa por todas os menus abertos exibindo-os
                # Renderiza texto a ser exibido
                texto = self.__config['fonte'].render('  ' * nivel + i, 0, self.__config['cor_fonte'](menus))
                self.screen.blit(texto, [0, y])  # Exibe o texto
                y += height  # Faz com que y fique abaixo do últmo item escrito

            for i, opcao in enumerate(opcoes):
                if i == selecionado:  # Se a opção tiver sido selecionada
                    texto = '  ' * nivel + '> ' + opcao
                else:
                    texto = '  ' * nivel + '  ' + opcao

                    # Renderiza o Texto a ser Exibido
                reder_texto = self.__config['fonte'].render(texto, 0, self.__config['cor_fonte'](menus))
                self.screen.blit(reder_texto, [0, y])  # Exibe o texto
                y += height  # Faz com que y fique abaixo do últmo item escrito

            pygame.display.flip()

        def escrever_opcoes2(opcoes: dict):
            """
            Exiba as opções de um dict
            {key}: {value}

            :param opcoes: Opções a ser mostradas
            """

            self.screen.fill(self.__config['menu'](menus))  # Pinta a tela
            y = 0  # Espaço já utilizada

            # TODO poderia exibir o menus assim Menu1 > Menu2 > Menu3
            for nivel, i in enumerate(menus):  # Passa por todas os menus abertos exibindo-os
                # Renderiza texto a ser exibido
                texto = self.__config['fonte'].render('  ' * nivel + i, 0, self.__config['cor_fonte'](menus))
                self.screen.blit(texto, [0, y])  # Exibe o texto
                y += height  # Faz com que y fique abaixo do últmo item escrito

            for i, k in enumerate(opcoes):  # Se a opção tiver sido selecionada
                if i == selecionado:
                    texto = '  ' * nivel + '> ' + k + str(opcoes[k])
                else:
                    texto = '  ' * nivel + '  ' + k + str(opcoes[k])  # key: value

                # Renderiza texto a ser exibido
                reder_texto = self.__config['fonte'].render(texto, 0, self.__config['cor_fonte'](menus))
                self.screen.blit(reder_texto, [0, y])  # Exibe o texto
                y += height  # Faz com que y fique abaixo do últmo item escrito

            pygame.display.flip()

        escrever_opcoes()  # Anota as opções
        while True:  # O menu tem eventos própios e por isso fica dentro de um while True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Clicou no botão fechar
                    quit(0)
                if event.type == pygame.KEYDOWN:  # Se alguma tecla tiver sido pressionada
                    if event.key == pygame.K_ESCAPE:  # Se a tecla pressionada for o Esc
                        self.blit_all()  # Exibe o tabuleiro
                        return  # Sai do loop e volta ao jogo
                    if event.key == pygame.K_UP:  # Se a tecla pressionada for seta para cima
                        if selecionado > 0:
                            selecionado -= 1  # O selecionador vai para cima
                            escrever_opcoes()  # Reexibe as opções para mostrar o novo item selecionado
                    if event.key == pygame.K_DOWN:  # Se a tecla pressionada for seta para baixo
                        if selecionado < len(opcoes) - 1:
                            selecionado += 1  # O selecionador vai para baixo
                            escrever_opcoes()  # Reexibe as opções para mostrar o novo item selecionado
                    if opcoes[selecionado] == 'Desfazer':  # Se a opção selecionada for de Desfazer
                        if event.key == pygame.K_RIGHT:  # Se a tecla pressionada for seta para direita
                            if desfazer < limite_desfazer:
                                desfazer += 1
                            else:  # Se desfazer chegou ou passou ao limite
                                desfazer = 1  # Pois se fosse 0 continuaria sendo Novo Jogo
                            escrever_opcoes()  # Reexibe as opções para mostrar as mudanças
                        if event.key == pygame.K_LEFT:  # Se a tecla pressionada for seta para esquerda
                            if desfazer > 0:
                                desfazer -= 1
                            else:  # Se desfazer é 0 ou menos
                                desfazer = limite_desfazer - 1  # Pois se fosse limite continuaria sendo Novo Jogo
                            escrever_opcoes()  # Reexibe as opções para mostrar as mudanças
                    if event.key == pygame.K_RETURN:  # Se a tecla pressionada for o Enter
                        opcao = opcoes[selecionado]  # Opção selecionada
                        if opcao == 'Configs':
                            selecionado = 0
                            configs = ['Default'] + all_configs('Xadrez') + ['Voltar']
                            menus.append('Configs')
                            escrever_opcoes1(configs)  # TODO Criar previews das caonfig

                            in_loop = True
                            while in_loop:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        quit(0)
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_ESCAPE:
                                            self.blit_all()
                                            return
                                        if event.key == pygame.K_UP:
                                            if selecionado > 0:
                                                selecionado -= 1
                                                escrever_opcoes1(configs)  # TODO Criar previews das caonfig
                                        if event.key == pygame.K_DOWN:
                                            if selecionado < len(configs) - 1:
                                                selecionado += 1
                                                escrever_opcoes1(configs)  # TODO Criar previews das caonfig
                                        if event.key == pygame.K_RETURN:
                                            if selecionado == 0:
                                                self.pacote_config = None
                                            elif selecionado < len(configs) - 1:
                                                pacote = configs[selecionado]
                                                self.pacote_config = pacote
                                            self.recolorir_tabuleiro()
                                            i, j = self.__click
                                            self.tabuleiro[i][j].fill(self.__config['click'](i, j))
                                            self.blit_all()

                                            in_loop = False
                            menus.pop()
                            selecionado = 0
                            escrever_opcoes()

                        elif opcao == 'Imagens':  # TODO Terminar imagens
                            selecionado = 0
                            imagens = all_imagens('Xadrez')
                            imagens.append('Voltar')
                            menus.append('Imagens')
                            escrever_opcoes1(imagens)

                            in_loop = True
                            while in_loop:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        quit(0)
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_ESCAPE:
                                            self.blit_all()
                                            return
                                        if event.key == pygame.K_UP:
                                            if selecionado > 0:
                                                selecionado -= 1
                                                escrever_opcoes1(imagens)
                                        if event.key == pygame.K_DOWN:
                                            if selecionado < len(imagens) - 1:
                                                selecionado += 1
                                                escrever_opcoes1(imagens)
                                        if event.key == pygame.K_RETURN:
                                            if selecionado < len(imagens) - 1:
                                                from Class.Recursos import GeradorRecursos
                                                pacote = imagens[selecionado]

                                                cores = {
                                                    'Branco Cor1 R: ': 100,
                                                    'Branco Cor1 G: ': 100,
                                                    'Branco Cor1 B: ': 100,
                                                    'Branco Cor2 R: ': 255,
                                                    'Branco Cor2 G: ': 255,
                                                    'Branco Cor2 B: ': 255,
                                                    'Preto  Cor1 R: ': 0,
                                                    'Preto  Cor1 G: ': 0,
                                                    'Preto  Cor1 B: ': 0,
                                                    'Preto  Cor2 R: ': 100,
                                                    'Preto  Cor2 G: ': 100,
                                                    'Preto  Cor2 B: ': 100,
                                                    'Aplicar': ''
                                                }
                                                escrever_opcoes2(cores)  # TODO Criar previews das cores
                                                menus.append('Cores')
                                                in_loop1 = True
                                                while in_loop1:

                                                    for event in pygame.event.get():
                                                        if event.type == pygame.QUIT:
                                                            quit(0)
                                                        if event.type == pygame.KEYDOWN:
                                                            if event.key == pygame.K_ESCAPE:
                                                                self.blit_all()
                                                                return
                                                            if event.key == pygame.K_UP:
                                                                if selecionado > 0:
                                                                    selecionado -= 1
                                                                    # TODO Criar previews das cores
                                                                    escrever_opcoes2(cores)
                                                            if event.key == pygame.K_DOWN:
                                                                if selecionado < len(cores) - 1:
                                                                    selecionado += 1
                                                                    # TODO Criar previews das cores
                                                                    escrever_opcoes2(cores)

                                                            if selecionado < len(opcoes) - 1:
                                                                if event.key == pygame.K_RIGHT:
                                                                    if cores[list(cores)[selecionado]] < 256:
                                                                        cores[list(cores)[selecionado]] += 1
                                                                        # TODO Criar previews das cores
                                                                        escrever_opcoes2(cores)
                                                                if event.key == pygame.K_LEFT:
                                                                    if cores[list(cores)[selecionado]] > 0:
                                                                        cores[list(cores)[selecionado]] -= 1
                                                                        # TODO Criar previews das cores
                                                                        escrever_opcoes2(cores)
                                                            if event.key == pygame.K_RETURN:
                                                                if selecionado < len(cores) - 1:
                                                                    pacote = configs[selecionado]
                                                                    self.pacote_config = pacote
                                                                self.recolorir_tabuleiro()
                                                                i, j = self.__click
                                                                self.tabuleiro[i][j].fill(self.__config['click'](i, j))
                                                                self.blit_all()

                                                                in_loop1 = False
                                                menus.pop()
                                                selecionado = 0
                                                escrever_opcoes()

                                                self.screen.fill(self.__config['menu'](menus))
                                                texto = self.__config['fonte'].render(
                                                    'Mudando Pacote', 0, self.__config['cor_fonte'](menus)
                                                )
                                                w, h = self.__config['fonte'].size('Mudando Pacote')
                                                meio_tela = self.quad_size * 4  # quad_size * 8 / 2 -> screen_size / 2
                                                meio = meio_tela - w / 2, meio_tela - h / 2
                                                self.screen.blit(texto, meio)
                                                pygame.display.flip()
                                                atualizar = GeradorRecursos('Xadrez', pacote)
                                                atualizar.gerar_recursos(
                                                    [[245, 245, 245], [255, 255, 255]],
                                                    [[0, 0, 0, ], [10, 10, 10, ]]
                                                )
                                                self.recursos.get_recurso(return_value=False)
                                            self.recolorir_tabuleiro()
                                            i, j = self.__click
                                            self.tabuleiro[i][j].fill(self.__config['click'](i, j))
                                            self.blit_all()

                                            in_loop = False
                            menus.pop()
                            selecionado = 0
                            escrever_opcoes()
                            pass

                        elif opcao == 'Fontes':  # TODO Implementar fontes
                            self.fonte = 'Consolas.ttf'
                            pass
                        elif opcao == 'Desfazer':  # FIXME Desfazer promoção
                            if 0 < desfazer < limite_desfazer:
                                print('desfazer')
                                self.xadrez.desfazer(desfazer)
                            else:
                                print('novo jogo')
                                self.xadrez.reposicionar_pecas()
                            self.recolorir_tabuleiro()
                            i, j = self.__click
                            self.tabuleiro[i][j].fill(self.__config['click'](i, j))
                            self.blit_all()
                            self.blit_all()
                            return
                        elif opcao == 'Voltar':
                            self.blit_all()
                            return
                        elif opcao == 'Sair':
                            quit(0)
                        else:
                            raise Exception('Opcao nao encontrada')

    def __on_click(self, event):
        if event.button == 1:

            if self.__click[0] is None:
                self.__on_click_promocao(event)

            m = int(event.pos[0] / self.quad_size)
            n = int(event.pos[1] / self.quad_size)
            x, y = self.__click

            aux = self.xadrez.movimentar_peca([x, y], [m, n])
            self.__click = m, n

            if aux is None:
                self.recolorir_tabuleiro()

                self.tabuleiro[x][y].fill(self.__config['quadrado'](x, y))
                self.tabuleiro[m][n].fill(self.__config['click'](m, n))
                if self.xadrez.tabuleiro[m][n]:
                    movimentos = self.xadrez.get_movimentos(m, n)
                    for i, line in enumerate(movimentos):
                        for j, b in enumerate(line):
                            if b:
                                if self.xadrez.tabuleiro[i][j]:
                                    self.tabuleiro[i][j].fill(self.__config['captura'](i, j))
                                else:
                                    self.tabuleiro[i][j].fill(self.__config['movimento'](i, j))
                self.blit_all()
            elif aux == 'promocao':
                self.__on_click_promocao_ecolha(event)

        if event.button == 3:
            self.menu()
            pass
            # opções

    def __on_click_promocao(self, event):
        from Class.PecasXadrez import nome_pecas
        nomes = [i for i in nome_pecas() if i not in ['Rei', 'Peao']]
        _, m, n = self.__click
        i = int(event.pos[0] / self.tmp_size)
        j = int(event.pos[1] / self.tmp_size)
        del self.tmp_size
        peca_por_linha = 2  # 4 Pecas ** (1/2) para formar um quadrado
        nome = nomes[i * peca_por_linha + j]
        self.xadrez.promocao(nome, [m, n])
        self.__click = m, n

    def __on_click_promocao_ecolha(self, event):
        from Class.PecasXadrez import nome_pecas
        nomes = [i for i in nome_pecas() if i not in ['Rei', 'Peao']]
        peca_por_linha = 2  # 4 Pecas ** (1/2) para formar um quadrado
        size = self.quad_size * 4  # quad_size * 8 / 2 -> screen_size / 2
        self.tmp_size = size
        for i in range(peca_por_linha):
            for j in range(peca_por_linha):
                quad = pygame.Surface([size, size])
                quad.fill(self.__config['quadrado'](i, j))
                key = '{}_{}'.format(
                    nomes[int(i * peca_por_linha + j)], 'branco' if self.xadrez.vez else 'preto'
                )
                img = self.recursos.recursos[key]
                rect = pygame.Rect([0, 0], [size, size])
                img = pygame.transform.scale(img, rect.size)
                quad.blit(img, rect)
                self.screen.blit(quad, [size * i, size * j])
                pygame.display.flip()
        aux = [None]
        aux.extend(self.__click)
        self.__click = aux

    def criar_tabuleiro(self):
        tabuleiro = [[None] * 8 for _ in range(8)]

        for i, line in enumerate(tabuleiro):
            for j in range(len(line)):
                tabuleiro[i][j] = self.quad()
                tabuleiro[i][j].fill(self.__config['quadrado'](i, j))
        return tabuleiro

    def recolorir_tabuleiro(self):
        for i, line in enumerate(self.tabuleiro):
            for j in range(len(line)):
                self.tabuleiro[i][j].fill(self.__config['quadrado'](i, j))
        self.blit_all()

    def blit_all(self):
        # Exibe as pecas no tabuleiro
        recursos = self.recursos.recursos
        for i, line in enumerate(self.xadrez.tabuleiro):
            for j, peca in enumerate(line):
                if peca:
                    nome = peca.nome_cor
                    img = recursos[nome]
                    rect = self.rect()
                    img = pygame.transform.scale(img, rect.size)
                    self.tabuleiro[i][j].blit(img, rect)

        # Exibe as tabuleiro na screen
        for i, line in enumerate(self.tabuleiro):
            for j, quad in enumerate(line):
                self.screen.blit(quad, [self.quad_size * i, self.quad_size * j])

        # Exibe o Titulo da tela
        pygame.display.set_caption(self.__config['titulo']())
        pygame.display.flip()

    def set_cores(self, *args, **kwargs):
        try:
            kwargs['branco'] = args[0]
            kwargs['preto'] = args[1]
            kwargs['click'] = args[2]
            kwargs['movimento'] = args[3]
        except:
            pass
        self.cores.update(**kwargs)

    def del_cores(self, *args):
        if args:
            for key in args:
                self.cores.pop(key)
        else:
            self.cores.clear()

    def set_config(self, **kwargs):
        for i in kwargs:
            if i not in list(self.__config):
                raise KeyError(i)
        try:
            kwargs['captura']
        except KeyError:
            kwargs['captura'] = kwargs['movimento']
        self.config.update(**kwargs)
