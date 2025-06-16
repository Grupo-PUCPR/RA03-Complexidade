import itertools
import multiprocessing
from time import time
from math import comb
from collections import defaultdict
import os

# Comentarios gemini para entender, mas basicamente indexa subgrupos -> grupos de numeros que sao englobados
# multithread
# alto custo de processamenteo e memoria RAM

# --- PARÂMETROS GERAIS DO PROBLEMA ---
# Altere para 14, 13, 12 ou 11
K_ALVO = 14

UNIVERSO_TOTAL = range(1, 26)
N_UNIVERSO = 25
K_APOSTA = 15
CUSTO_POR_APOSTA = 3.00

# --- ETAPA 1: CONSTRUÇÃO PARALELA DO ÍNDICE ---


#Complexidade geral: O(n.C(m,k)) ou O(n. (m!/k!(m-k)!))
def construir_indice_parcial(lote_de_apostas):
    mapa_parcial = defaultdict(list) #O(1)
    for aposta_s15 in lote_de_apostas: #O(n)
        for alvo_sk in itertools.combinations(aposta_s15, K_ALVO): #O(C(m,k)) -> m = tamanho de cada aposta | k = tamanho do sb alvo 
            mapa_parcial[alvo_sk].append(aposta_s15) # O(1)
    return mapa_parcial #(1)


#Complexidade geral: O(C(N,K)⋅C(m,k)) -> N=universo | K=sb aposta | m=K | k=sb alvo
def construir_indice_invertido_paralelo():
    num_processos = os.cpu_count() or 1 #O(1)
    print(f"ETAPA 1: Construindo Índice Invertido com {num_processos} processos...")#O(1)
    
    apostas_s15_gen = itertools.combinations(UNIVERSO_TOTAL, K_APOSTA) #O(1)
    
    total_apostas = comb(N_UNIVERSO, K_APOSTA) #O(1)
    print(f"Total de apostas: {total_apostas}") #O(1)
    tamanho_lote = (total_apostas // num_processos) + 1 #O(1)
    
    lotes = [] #O(1)
    lote_atual = [] #O(1)
    for aposta in apostas_s15_gen: #O(C(m,k)) -> m=tamanho de cada aposta | k=tamanho do sb alvo
        lote_atual.append(aposta) #O(1)
        if len(lote_atual) == tamanho_lote: #O(1)
            lotes.append(lote_atual) #O(1)
            lote_atual = [] #O(1)
    if lote_atual: #O(1)
        lotes.append(lote_atual) #O(1)

    #Complexidade do multiprocesso: O(C(N,K)⋅C(m,k)) 
    with multiprocessing.Pool(processes=num_processos) as pool: 
        resultados_parciais = pool.map(construir_indice_parcial, lotes) #Complexidade de cada processo O(l.C(m,k))-> l=tamanho do lote

    print("   ... Juntando os resultados parciais...") #O(1)
    mapa_sk_para_s15 = defaultdict(list) #O(1)
    #O(C(m,k)⋅p)
    for mapa_parcial in resultados_parciais: #O(p)
        for sk, lista_s15 in mapa_parcial.items(): #O(C(m,k))
            mapa_sk_para_s15[sk].extend(lista_s15) #O(1)
            
    return mapa_sk_para_s15 #O(1)


#O(C(N,K).C(K,k)²)
def resolver_com_guloso_otimizado():

    inicio_total = time() # O(1)

    mapa_sk_para_s15 = construir_indice_invertido_paralelo()#O(C(N,K)⋅C(K,k))
    print(f"Índice construído em {time() - inicio_total:.2f}s.\n") #O(1)

    print("ETAPA 2: Preparando estruturas para o loop guloso (Buckets)...")#O(1)
    
    universo_a_cobrir = set(mapa_sk_para_s15.keys()) #O(m,k)
    total_alvos = len(universo_a_cobrir) #O(1)
    
    pontuacao_maxima = comb(K_APOSTA, K_ALVO) #O(1)
    buckets = [set() for _ in range(pontuacao_maxima + 1)] #O(1)
    
    mapa_s15_para_pontuacao = {} #O(1)
    
    apostas_s15_todas = list(itertools.combinations(UNIVERSO_TOTAL, K_APOSTA)) #O(C(N,K))
    for aposta in apostas_s15_todas: #O(C(N,K))
        # No início, todas as apostas têm a pontuação máxima

        buckets[pontuacao_maxima].add(aposta)#O(1)
        mapa_s15_para_pontuacao[aposta] = pontuacao_maxima #O(1)
    
    print("Estruturas prontas.\n")# O(1)

    # ETAPA 3: Loop Guloso Otimizado com Buckets
    print("Cobrindo o universo", total_alvos)# O(1)
    print("ETAPA 3: Iniciando o Loop Guloso Otimizado...")# O(1)
    
    cobertura_final = []# O(1)
    pontuacao_atual = pontuacao_maxima# O(1)

    while universo_a_cobrir: #C(N,k) -> todas as possibilidades do universo
        while not buckets[pontuacao_atual]: #C(K,k) -> todas as possibilidades de 15,11
            pontuacao_atual -= 1 #O(1)
        
        melhor_aposta = buckets[pontuacao_atual].pop()#O(1)
        cobertura_final.append(melhor_aposta)#O(1)

        alvos_cobertos_nesta_rodada = {
            sk for sk in itertools.combinations(melhor_aposta, K_ALVO) if sk in universo_a_cobrir #O(C(K,k)) - for | O(C(K, k)) - if
        }
        

        #No geral: O(C(K,k). A_sk)
        for alvo_coberto in alvos_cobertos_nesta_rodada: #O(C(K,k))
            for aposta_afetada in mapa_sk_para_s15[alvo_coberto]:#O(A_sk) -> A_sk = média de apostas que foram cobertas
                if aposta_afetada in mapa_s15_para_pontuacao: #O(1)
                    pontuacao_antiga = mapa_s15_para_pontuacao[aposta_afetada]#O(1)
                    buckets[pontuacao_antiga].discard(aposta_afetada)#O(1)
                    
                    nova_pontuacao = pontuacao_antiga - 1#O(1)
                    buckets[nova_pontuacao].add(aposta_afetada)#O(1)
                    mapa_s15_para_pontuacao[aposta_afetada] = nova_pontuacao#O(1)
        
        universo_a_cobrir.difference_update(alvos_cobertos_nesta_rodada) #O(1)
        del mapa_s15_para_pontuacao[melhor_aposta] #O(1)
        

    # Resultados Finais
    fim_total = time()
    print("\n" + "="*50)
    print("Cobertura de Conjuntos Finalizada!")
    print(f"O subconjunto SB{K_APOSTA}_{K_ALVO} encontrado contém {len(cobertura_final)} apostas.")
    
    custo_total = len(cobertura_final) * CUSTO_POR_APOSTA
    print(f"Custo total para as {len(cobertura_final)} apostas: R$ {custo_total:,.2f}")
    print(f"Tempo total de execução: {fim_total - inicio_total:.2f} segundos.")
    print("="*50)

    return cobertura_final

if __name__ == "__main__":
    for i in resolver_com_guloso_otimizado():
        print(i)