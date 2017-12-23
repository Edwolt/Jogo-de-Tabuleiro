import pygame

from Class.Recursos import Recursos
from Class.Xadrez import Xadrez


class Tela:
    @property
    def quad(self):
        return pygame.Surface([self.quad_size, self.quad_size])

    @property
    def rect(self):
        return pygame.Rect([0, 0], [self.quad_size, self.quad_size])

    def __init__(self, size=800, framerate=60, pacote='Default'):
        pygame.init()
        self.screen = pygame.display.set_mode([size, size])

        self.xadrez = Xadrez()
        self.recursos = Recursos(pacote, 'Xadrez')
        self.__clock = pygame.time.Clock()

        self.tabuleiro = None
        self.__click = 0, 0
        self.framerate = framerate
        self.quad_size = size / 8
        self.cores = dict()
        self.set_config(
            branco=[255, 255, 255],
            preto=[0, 0, 0],
            click=[255, 0, 0],
            movimento=[0, 255, 255]
        )

        self.config = {
            'quadrado': lambda cores, i, j: cores['branco'] if (i + j) % 2 == 0 else self.cores['preto'],
            'movimento': lambda cores, i, j: cores['movimento'],
            'click': lambda cores, i, j: cores['click'],
            'titulo': lambda vez: 'Xadrez : ' + ('Branco' if vez else 'Preto')
        }
        self.__config = {
            'quadrado': lambda i, j: self.config['quadrado'](self.cores, i, j),
            'movimento': lambda i, j: self.config['movimento'](self.cores, i, j),
            'click': lambda i, j: self.config['click'](self.cores, i, j),
            'titulo': lambda: self.config['titulo'](self.xadrez.vez)
        }

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
            self.recolorir_tabuleiro()
            i = int(event.pos[0] / self.quad_size)
            j = int(event.pos[1] / self.quad_size)

            x, y = self.__click
            self.__click = i, j
            self.tabuleiro[x][y].fill(self.__config['quadrado'](x, y))
            self.tabuleiro[i][j].fill(self.__config['click'](i, j))
            self.xadrez.movimentar_peca([x, y], [i, j])
            if self.xadrez.tabuleiro[i][j]:
                movimentos = self.xadrez.get_movimentos(i, j)
                for i, line in enumerate(movimentos):
                    for j, b in enumerate(line):
                        if b:
                            self.tabuleiro[i][j].fill(self.__config['movimento'](i, j))
            self.blit_all()
            self.blit_all()
        if event.button == 3:
            self.blit_all()
            pass
            # opções

    def criar_tabuleiro(self):
        tabuleiro = [None] * 8
        for i in range(len(tabuleiro)):
            tabuleiro[i] = [None] * 8

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

    def set_config(self, *args, **kwargs):
        try:
            kwargs['branco'] = args[0]
            kwargs['preto'] = args[1]
            kwargs['click'] = args[2]
            kwargs['movimento'] = args[3]
        except:
            pass
        self.cores.update(**kwargs)

    def del_config(self, *args):
        if args:
            for key in args:
                self.cores.pop(key)
        else:
            self.cores.clear()
