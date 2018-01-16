import json


class Save:
    jogo = property()

    @jogo.setter
    def jogo(self, value):
        self.path = f'Recursos/{value}/save.json'

    def __init__(self, jogo):
        self.path = f'Recursos/{jogo}/save.json'
        self.dados = dict()
        self.keys = lambda: self.dados.keys()

    def salvar(self, dados=None):
        file = open(self.path, 'w')
        if dados:
            json.dump(dados, file)
        else:
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
