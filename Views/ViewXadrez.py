import pygame

from Class.Recursos import Recursos
from Class.Xadrez import Xadrez


class Tela:
    pacote_img = property()

    @pacote_img.setter
    def pacote_img(self, value):
        self.recursos.pacote = value

    pacote_cor = property()

    @pacote_cor.setter
    def pacote_cor(self, value):
        self.recursos.cores = value

    @property
    def quad(self):
        return pygame.Surface([self.quad_size, self.quad_size])

    @property
    def rect(self):
        return pygame.Rect([0, 0], [self.quad_size, self.quad_size])

    def __init__(self, size=800, framerate=60, pacote_img='Default', pacote_cor=None):
        pygame.init()
        self.screen = pygame.display.set_mode([size, size])

        self.xadrez = Xadrez()
        self.recursos = Recursos('Xadrez', pacote_img, pacote_cor)
        self.__clock = pygame.time.Clock()

        self.tabuleiro = None
        self.__click = 0, 0
        self.framerate = framerate
        self.quad_size = size / 8
        self.cores = dict()
        self.set_cores(
            branco=[255, 255, 255],
            preto=[0, 0, 0],
            click=[255, 0, 0],
            movimento=[0, 255, 255]
        )

        self.config = {
            'quadrado': lambda cores, i, j: cores['branco'] if (i + j) % 2 == 0 else self.cores['preto'],
            'click': lambda cores, i, j: cores['click'],
            'movimento': lambda cores, i, j: cores['movimento'],
            'captura': lambda cores, i, j: self.config['movimento'](cores, i, j),
            'titulo': lambda vez: 'Xadrez : ' + ('Branco' if vez else 'Preto')
        }
        self.__config = {
            'quadrado': lambda i, j: self.config['quadrado'](self.cores, i, j),
            'click': lambda i, j: self.config['click'](self.cores, i, j),
            'movimento': lambda i, j: self.config['movimento'](self.cores, i, j),
            'captura': lambda i, j: self.config['captura'](self.cores, i, j),
            'titulo': lambda: self.config['titulo'](self.xadrez.vez)
        }
        if self.recursos.config and self.recursos.config.cores:
            if self.recursos.config.del_cores:
                self.del_cores()
            self.set_cores(**self.recursos.config.cores)

        if self.recursos.config and self.recursos.config.config:
            self.set_config(**self.recursos.config.config)

    def novo_jogo(self):
        self.xadrez.reposicionar_pecas()
        self.tabuleiro = self.criar_tabuleiro()
        self.__click = 0, 0
        self.blit_all()
        while True:
            self.main()

    def main(self):
        self.eventos()
        self.__clock.tick(self.framerate)
        pass

    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.__on_click(event)

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
            self.blit_all()
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
        size = self.quad_size * 8 / 2
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
                tabuleiro[i][j] = self.quad
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
                    rect = self.rect
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
