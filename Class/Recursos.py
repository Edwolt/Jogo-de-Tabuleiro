import cv2
import numpy
import pygame

from Class.PecasXadrez import nome_pecas


class Recursos:
    pacote = property()

    @pacote.getter
    def pacote(self):
        return self.__pacote
        pass

    @pacote.setter
    def pacote(self, value):
        self.pacote = value
        self.recursos = self.get_recurso()
        pass

    config = property()

    @config.getter
    def config(self):
        return self.__config

    @config.setter
    def config(self, value):
        if value:
            import importlib
            self.__config = importlib.import_module(f'Pacotes.Xadrez.Config.{value}')

    # Requer pacote para atualizar recursos
    def __init__(self, jogo, config=None):
        self.jogo = jogo
        self.recursos = self.get_recurso()
        self.__config = None
        if config:
            import importlib
            self.__config = importlib.import_module(f'Pacotes.Xadrez.Config.{config}')

    def get_recurso(self, return_value=True):
        recursos = dict()
        for nome, caminho in self.get_caminhos():
            recursos.__setitem__(nome, pygame.image.load(f'{caminho}.png'))
        if return_value:
            return recursos
        else:
            self.recursos = recursos

    # retorna todos os caminhos necessarios -> [[nome, caminho],[nome, caminho], ... ]
    def get_caminhos(self):
        for nome in nome_pecas():
            yield f'{nome}_branco', f'Recursos/{self.jogo}/{nome}_branco'
            yield f'{nome}_preto', f'Recursos/{self.jogo}/{nome}_preto'


class GeradorRecursos:
    def __init__(self, jogo, pacote):
        self.jogo = jogo
        self.pacote = pacote
        self.size = 216

    # cor = [X, X, X]
    def gerar_paleta(self, cor1, cor2):
        r = numpy.linspace(cor1[0], cor2[0], 256)
        g = numpy.linspace(cor1[1], cor2[1], 256)
        b = numpy.linspace(cor1[2], cor2[2], 256)

        r = numpy.tile(r.reshape(256, 1), 256)
        g = numpy.tile(g.reshape(256, 1), 256)
        b = numpy.tile(b.reshape(256, 1), 256)

        r = numpy.uint8(r)
        g = numpy.uint8(g)
        b = numpy.uint8(b)

        return numpy.dstack((b, g, r))

    # cor = [X, X, X]
    def gerar_imagem(self, img, cor1, cor2):
        cor1.append(255)
        cor2.append(255)
        paleta = self.gerar_paleta(cor1, cor2)
        img_cor = numpy.zeros((img.shape[0], img.shape[1], 4))
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                pixel = img[i][j]
                img_cor[i][j] = [*paleta[pixel][0][0], pixel[3]]

        img_cor = numpy.uint8(img_cor)
        return img_cor

    # grad = [[X, X, X], [X, X, X]]
    def gerar_recursos(self, grad1, grad2):
        for peca in nome_pecas():
            img = cv2.imread(f'Pacotes/{self.jogo}/Imagens/{self.pacote}/{peca}.png', cv2.IMREAD_UNCHANGED)
            # img = gerar_imagem(f'Pacotes/{pacote}/{peca}.png', grad1[0], grad1[1])
            branco = self.gerar_imagem(img, grad1[0], grad1[1])

            cv2.imwrite(f'Recursos/{self.jogo}/{peca}_branco.png', cv2.resize(branco, (self.size, self.size)))
            # img = gerar_imagem(f'Pacotes/{pacote}/{peca}.png', grad2[0], grad2[1])
            preto = self.gerar_imagem(img, grad2[0], grad2[1])
            cv2.imwrite(f'Recursos/{self.jogo}/{peca}_preto.png', cv2.resize(preto, (self.size, self.size)))
