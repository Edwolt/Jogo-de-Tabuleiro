import json


class Save:
    jogo = property()

    @jogo.setter
    def jogo(self, value):
        self.path = f'{value}/save.json'

    def __init__(self, jogo):
        self.path = f'{jogo}/save.json'
        self.dados = dict()
        self.keys = lambda: self.dados.keys()

    def salvar(self, *kwargs):
        file = open(self.path, 'w')
        json.dump(self.dados, file)

    def carregar(self):
        try:
            file = open(self.path, 'r')
            dados = json.load(file)
        except (OSError, IOError):
            file = open(self.path, 'w')
            file.close()
            dados = dict()

        self.dados = dados
