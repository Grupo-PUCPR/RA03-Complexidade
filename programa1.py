import random
from itertools import combinations

numeros = [i for i in range(1, 6)]

def sb_num(tamanho):
    return list(combinations(numeros, tamanho))

sb3 = sb_num(3)
sb2 = sb_num(2)
print(sb3, '\n', sb2) 

subconjunto = []
sb3_copy = sb3.copy()
sb2_copy = sb2.copy()  

for _ in sb3:
    combinacao = random.choice(sb3_copy)
    sb3_copy.remove(combinacao)
    set_combinacao = set(combinacao) # faço um set (coleção de itens únicos)
    remover = []  
    for comb2 in sb2_copy:
        set_comb2 = set(comb2)
        #se minha comb menor tem na combinação maior
        if set_comb2.issubset(set_combinacao):
            remover.append(comb2)
    
    #remove cada item do meu sb2
    for item in remover:
        sb2_copy.remove(item)

    #só add a combinação a solução se eu tiver itens para remover
    if remover: 
        subconjunto.append(combinacao)

print("Subconjuntos escolhidos:", subconjunto)
