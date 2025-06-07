import random
from itertools import combinations

numeros = [i for i in range(1, 26)]

def sb_num(tamanho):
    return list(combinations(numeros, tamanho))