from sb import sb_num
import random
import numpy as np

#função para verificar se a combinação tem sequência maior que 3 elementos
def tem_sequencia_longa(comb, min_tamanho=3):
    tamanho = 1
    tamanho_max = 1
    for i in range(len(comb) - 1):
        if comb[i] + 1 == comb[i+1]:
            tamanho += 1
            tamanho_max = max(tamanho_max, tamanho) #pega o maior tamanho
        else:
            tamanho = 1
    return tamanho_max >= min_tamanho

# compara com lista combinacoes, se alguma for 80% igual, retorna True
def compara_combinacoes(comb_set, combinacoes_sets, limiar_similaridade=0.8):
    for c_set in combinacoes_sets:
        intersecao = len(comb_set & c_set)
        similaridade = intersecao / len(comb_set)
        if similaridade >= limiar_similaridade:
            return True
    return False

# remove números muito próximos, que a média fique abaixo de um limite
def distancia_media_baixa(comb, limite=6):
    comb = sorted(comb)
    diffs = [comb[i+1] - comb[i] for i in range(len(comb)-1)]
    return np.mean(diffs) < limite


sb15 = sb_num(3)
sb14 = sb_num(2)

faltando_cobrir = set(tuple(sorted(c)) for c in sb14)
subconjunto = []

random.shuffle(sb15)  # Embaralha uma vez
while faltando_cobrir:

    combinacao = random.choice(sb15)
    sb15.remove(combinacao) #garante que não vai pegar a msm dnv

    set_combinacao = set(combinacao)

    #Filtros
    if tem_sequencia_longa(combinacao):
        continue
    if distancia_media_baixa(combinacao):
        continue
    if compara_combinacoes(set_combinacao, [set(sc) for sc in subconjunto]):
        continue

    # Verifica o que essa combinação cobre de sb14
    cobre = set()
    for comb2 in list(faltando_cobrir):
        if set(comb2).issubset(set_combinacao):
            cobre.add(comb2)

    if cobre:
        subconjunto.append(combinacao)
        faltando_cobrir -= cobre  # remove o que já foi coberto

    if not faltando_cobrir:
        break


print("Cobriu todos os subonjuntos?", not faltando_cobrir, "Subconjuntos escolhidos:", len(subconjunto))
