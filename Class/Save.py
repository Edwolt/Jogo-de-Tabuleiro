import json


class Save:
    """Salva dados"""

    jogo = property()

    @jogo.setter
    def jogo(self, value: str):
        """
        :param value: Nome do jogo
        """

        self.path = f'Recursos/{value}/save.json'

    def __init__(self, jogo):
        """
        :param jogo: Nome do Jogo
        """

        self.path = f'Save/{jogo}.json'  # Caminho até o save
        self.dados = dict()
        self.keys = lambda: self.dados.keys()

    def salvar(self, **kwargs):
        file = open(self.path, 'w')
        if len(kwargs) == 0:
            json.dump(self.dados, file)
        else:
            json.dump(kwargs, file)

    def carregar(self):
        try:
            file = open(self.path, 'r')
            dados = json.load(file)
        except (OSError, IOError):
            file = open(self.path, 'w')
            file.close()
            dados = dict()

        self.dados = dados
