from random import randint as random

del_cores = False

cores = {
    'preto': [random(0, 255), random(0, 255), random(0, 255)],
    'branco': [random(0, 255), random(0, 255), random(0, 255)],
    'click': [random(0, 255), random(0, 255), random(0, 255)],
    'movimento': [random(0, 255), random(0, 255), random(0, 255)]
}

config = None
