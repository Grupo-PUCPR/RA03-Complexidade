import heapq
import numpy as np
from sb import sb_num
import random

sb15 = sb_num(15)
sb14 = sb_num(14)

subconjunto = []
sb15_copy = sb15.copy()
sb14_copy = sb14.copy()  

top_comb = []  # heap para guardar as melhores combinações
k = 10  # número máximo de combinações que quero guardar

def score(comb):
    return np.std(comb)  # exemplo: maior desvio padrão (mais espalhada)

for comb in sb15_copy:
    s = score(comb)
    heapq.heappush(top_comb, (s, comb))  # insere no heap como tupla (score, combinação)

    if len(top_comb) > k:
        heapq.heappop(top_comb)  # remove a combinação com menor score (menos interessante)

