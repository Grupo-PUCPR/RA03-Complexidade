from itertools import combinations
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

# remove se o desvio padrão for muito 
def desvio_espacamento(comb, limite=2):
    comb = sorted(comb)
    diffs = [comb[i+1] - comb[i] for i in range(len(comb)-1)]
    return np.std(diffs) > limite

# remove números muito próximos, que a média fique abaixo de um limite
def distancia_media_baixa(comb, limite=8):
    comb = sorted(comb)
    diffs = [comb[i+1] - comb[i] for i in range(len(comb)-1)]
    return np.mean(diffs) < limite

def regras(comb):
    return not tem_sequencia_longa(comb) or distancia_media_baixa(comb) or desvio_espacamento(comb)

def cobrir_subconjuntos(total_elementos, tamanho_sub, tamanho_alvo):
    todos_alvo = set(combinations(range(1, total_elementos + 1), tamanho_alvo))
    candidatos = list(combinations(range(1, total_elementos + 1), tamanho_sub))
    random.shuffle(candidatos)

    cobertura = set()
    subconjuntos_usados = []

    for _ in candidatos:
        candidato = random.choice(candidatos)
        if not regras(candidato):
            continue
            
        subconjuntos_de_alvo = set(combinations(candidato, tamanho_alvo))
        novos = subconjuntos_de_alvo - cobertura

        if novos:
            subconjuntos_usados.append(candidato)
            cobertura.update(novos)

        if len(cobertura) == len(todos_alvo):
            break

    return subconjuntos_usados

resultado = cobrir_subconjuntos(25,15,14)
#resultado1 = cobrir_subconjuntos(25,14,13)
#resultado2 = cobrir_subconjuntos(25,13,12)
#resultado3 = cobrir_subconjuntos(25,12,11)


print(f"Total de subconjuntos de 15 usados: {len(resultado)}")
print(len(resultado))
#print(len(resultado1))
#print(len(resultado2))
#print(len(resultado3))