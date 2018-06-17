"""
Contém as seguintes classes para utilizar os recursos (Imagens e Configd)
    * Recurso -> Guarda todos os recursos em seus atributos
    * GeradorRecursos -> Serve para mudar as imagens
"""

import cv2
import numpy
import pygame

from Class.PecasXadrez import nome_pecas


def all_configs(jogo: str) -> list:
    """
    :param jogo: Nome do jogo
    :return: list de todos os nomes de imagens dentro da pasta Pacotes/{jogo}/Configs/
    """

    import glob
    return [i.split('/')[-1][:-3] for i in glob.glob(f'Pacotes/{jogo}/Config/*.py')]


def all_imagens(jogo: str) -> list:
    """
    :param jogo: Nome do jogo
    :return: list de todos os nomes de imagens dentro da pasta Pacotes/{jogo}/Imagens/
    """

    import os
    return os.listdir(f'Pacotes/{jogo}/Imagens')


class Recursos:
    """
    Retém Imagens de todas as Pecas para ser utilizada com pygame
    Retém um módulo contendo as Configs
    """

    config = property()

    @config.getter
    def config(self):
        """
        :return: módulo com a config de uma das seguintes formas:
            * (vars -> del_cores: bool, cores: dict, configs: dict)
            * (vars -> del_cores: bool, cores: dict)
            * (vars -> configs: dict)
        """

        return self.__config

    @config.setter
    def config(self, value: str):
        """
        Então importe o módulo que está dentro da pasta Pacotes/{jogo}/Config
        E coloque o módulo dentro atributo config

        :param value: nome do módulo (atribuição)
        """
        if value:
            import importlib
            self.__config = importlib.import_module(f'Pacotes.{self.jogo}.Config.{value}')

    def __init__(self, jogo: str, config=None, get_recursos=True):
        """
        :param jogo: Define nome do jogo (pastas onde está tudo)
        :param config: Define qual com Config começar
        :param get_recursos: Define se precisa de capturar recursos (corrige erro de não ler Recursos)
        """
        self.jogo = jogo
        if get_recursos:
            self.recursos = self.get_recurso()
        self.__config = None  # Valor property config
        if config:
            import importlib
            self.__config = importlib.import_module(f'Pacotes.Xadrez.Config.{config}')

    def get_recurso(self, return_value: bool = True):
        """
        :param return_value: Define se o resultado será retornado ou não, Por padrão o valor é True
        :return: list de Surfaces (Surfaces do pygame) com as imagens das pecas
        """
        recursos = dict()
        for nome, caminho in self.get_caminhos():
            recursos.__setitem__(nome, pygame.image.load(f'{caminho}.png'))
        if return_value:
            return recursos
        else:
            self.recursos = recursos

    def get_caminhos(self):
        """
        Retorne o caminho de todas as imgens na pasta Recursos/{jogo}

        :return: interable no formato ([nome, caminho],[nome, caminho], ... )
        """
        for nome in nome_pecas():
            yield f'{nome}_branco', f'Recursos/{self.jogo}/{nome}_branco'
            yield f'{nome}_preto', f'Recursos/{self.jogo}/{nome}_preto'


class GeradorRecursos(Recursos):
    """
    Subclasse de Recursos
    Permite gerar novamente as imagens do recursos
    """

    def __init__(self, jogo: str, pacote: str):
        Recursos.__init__(self, jogo, None, False)
        self.pacote = pacote
        self.size = 512  # Tamanho das imagen geradas

    def gerar_paleta(self, cor1: tuple, cor2: tuple):
        """
        Gera uma paleta de cores

        :param cor1: (R, G, B)
        :param cor2: (R, G, B)
        :return: paleta de cores da cor1 a cor2
        """

        # Cria array de com valores de um numero a outro, tendo 256 elementos
        r = numpy.linspace(cor1[0], cor2[0], 256)
        g = numpy.linspace(cor1[1], cor2[1], 256)
        b = numpy.linspace(cor1[2], cor2[2], 256)

        #
        r = numpy.tile(r.reshape(256, 1), 256)
        g = numpy.tile(g.reshape(256, 1), 256)
        b = numpy.tile(b.reshape(256, 1), 256)

        #
        r = numpy.uint8(r)
        g = numpy.uint8(g)
        b = numpy.uint8(b)

        #
        return numpy.dstack((b, g, r))

    def gerar_imagem(self, img, cor1: tuple, cor2: tuple):
        """
        Use uma imagem qualquer para gerar outra colorida de acordo com os parametros cor1 e cor2

        :param img: resultado do método cv2.imread()
        :param cor1: (R, G, B)
        :param cor2: (R, G, B)
        :return: Imagem colorida
        """

        paleta = self.gerar_paleta(cor1, cor2)
        img_cor = numpy.zeros((img.shape[0], img.shape[1], 4))  # Imagem toda preta
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                pixel = img[i][j]  # pixel na linha i e coluna j da imagem original

                # Com paleta[pixel][0][0] o pixel de img_cor recebe um valor modificado de acordo com o valor de pixel
                img_cor[i][j] = paleta[pixel][0][0].tolist() + [pixel[3]]  # pixel[3] pega o alpha da imagem original

        img_cor = numpy.uint8(img_cor)  #
        return img_cor

    def gerar_recursos(self, grad1: tuple, grad2: tuple):
        """
        Gera imagens coloridas de acordo com os paramentos grad e as salva em Recursos/{jogo} para ser usado durante a
execução

        :param grad1: ((R, G, B), (R, G, B)) -> Gera paleta das Pecas brancas
        :param grad2: ((R, G, B), (R, G, B)) -> Gera paleta das Pecas pretas

        Cada grad gera uma paleta para ser usada na coloração das imagens
        Esse método só abre imagens no formato png
        Esse métodos espera que as imagens estejam da seguinte forma Pacotes/{jogo}/Imagens/{pacote}/{peca}.png
            * Sendo que {jogo} já foi armazenado na Classe através do __init__ e corresponde ao nome do jogo escolhido
            * Sendo que {pacote} já foi armazenado na Classe através do __init__ e corresponde ao pacote com as imagens
            * Sendo {peca} o nome da peca
        """
        print(f'Cores Branco: {grad1}\nCores Preto: {grad2}\n')

        for peca in nome_pecas():
            # Lê a imagem - cv2.IMREAD_UNCHANGED faz com que seja reconhecido o alfa
            img = cv2.imread(f'Pacotes/{self.jogo}/Imagens/{self.pacote}/{peca}.png', cv2.IMREAD_UNCHANGED)

            branco = self.gerar_imagem(img, grad1[0], grad1[1])  # Gera a versão branca da peca
            # Muda o tamanho da imagem de acordo com o atributo size e salva a imagem
            cv2.imwrite(f'Recursos/{self.jogo}/{peca}_branco.png', cv2.resize(branco, (self.size, self.size)))
            print(f'{peca} branco')

            preto = self.gerar_imagem(img, grad2[0], grad2[1])  # Gera a versão preta da peca
            # Muda o tamanho da imagem de acordo com o atributo size e salva a imagem
            cv2.imwrite(f'Recursos/{self.jogo}/{peca}_preto.png', cv2.resize(preto, (self.size, self.size)))
            print(f'{peca} preto')
