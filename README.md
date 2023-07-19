Refiz esse projeto em [outro repositório](https://github.com/Edwolt/Jogo-de-Tabuleiro-2),
para usar melhores técnicas de programação

# Jogo de Tabuleiro
É simplesmente um jogo de Xadrez feito em python

![xadrez](images/Xadrez.png)
![xadrez marrom](images/Xadrez_marrom.png)

Atenção: para rodar o porjeto é necessário atender as seguintes dependências
* pygame
* numpy
* cv2

Antes de iniciar o jogo
é nescessário que a pasta Recursos/Xadrez
contenha as imagens das peças
com os nomes definidos nas classes em PecasXadrez.py

Para fazer isso crie a pasta onde serão salvas as imagens:

```sh
mkdir Recursos/Xadrez
```

Depois rode o script para criar as imagens:
```sh
python3 RedefinirRecursos.py
```

Depois disso é possível iniciar o jogo com o comando:
```sh
python3 Jogar.pyw
```

# Funcionalidade
- Movimentação
  - Movimentos das peças
  - Movimento especiais (roque e en passant)
  - Obs: Não foi implementado o xeque mate nem o rei afogado
- Desfazer movimentos
- Pacotes: É possível mudas as cores das casas
  do tabuleiro para diferentes configurações
