from Class.Recursos import GeradorRecursos

# Cores Brancas
cor1 = [100, 100, 100]
cor2 = [255, 255, 255]
grad1 = [cor1, cor2]

# Cores Pretas
cor1 = [0, 0, 0]
cor2 = [100, 100, 100]
grad2 = [cor1, cor2]

atualizar = GeradorRecursos('Xadrez', 'Default')

atualizar.gerar_recursos(grad1, grad2)
