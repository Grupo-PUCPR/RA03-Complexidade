import itertools
from time import time
from math import comb
from collections import defaultdict

# Comentarios gemini para entender, mas basicamente indexa subgrupos -> grupos de numeros que sao englobados
# multithread
# alto custo de processamenteo e memoria RAM

# --- PARÂMETROS GERAIS DO PROBLEMA ---
# Altere este valor para resolver para S14, S13, S12 ou S11 (Programas 2 a 5)
K_SUBGRUPOS_A_COBRIR = 14  # Exemplo: 14 para o PROGRAMA 2 (cobrir S14)

UNIVERSO_TOTAL = set(range(1, 26))
N_UNIVERSO = 25
K_APOSTA_S15 = 15
CUSTO_POR_APOSTA = 3.00

def resolver_cobertura_com_indice_invertido():
    print("--- Iniciando a resolução com otimização de Índice Invertido ---")
    
    # 1. Gerar o universo a ser coberto (igual ao anterior)
    universo_a_cobrir = {
        comb 
        for comb in itertools.combinations(UNIVERSO_TOTAL, K_SUBGRUPOS_A_COBRIR)
    }
    total_elementos_universo = len(universo_a_cobrir)
    print(f"Universo Sk (k={K_SUBGRUPOS_A_COBRIR}) gerado com {total_elementos_universo:,} combinações.")

    # --- ETAPA LENTA E INTENSIVA DE MEMÓRIA: CONSTRUÇÃO DO ÍNDICE ---
    print("Construindo o índice invertido (mapa Sk -> S15)... Esta etapa pode demorar.")
    inicio_index = time()

    mapa_sk_para_s15 = defaultdict(list)
    contagem_cobertura_s15 = {} # Usaremos um dicionário como nosso contador de "pontos"

    # Itera sobre todas as S15 para popular os mapas
    for aposta_s15 in itertools.combinations(UNIVERSO_TOTAL, K_APOSTA_S15):
        # Inicializa a contagem de cobertura para esta aposta
        contagem_cobertura_s15[aposta_s15] = comb(K_APOSTA_S15, K_SUBGRUPOS_A_COBRIR)
        # Popula o índice invertido
        for sk in itertools.combinations(aposta_s15, K_SUBGRUPOS_A_COBRIR):
            mapa_sk_para_s15[sk].append(aposta_s15)
            
    print(f"Índice construído em {time() - inicio_index:.2f}s.")
    print("-" * 50)
    
    # --- NOVO LOOP GULOSO - MUITO MAIS RÁPIDO ---
    cobertura_final = []
    iteracao = 1
    
    while universo_a_cobrir:
        inicio_iteracao = time()

        # 1. Encontrar a melhor aposta é agora uma busca pelo maior valor no dicionário de contagens
        # Esta operação é muito mais rápida do que o laço 'for' de 3.2 milhões de itens
        if not contagem_cobertura_s15: break # Segurança
        melhor_aposta = max(contagem_cobertura_s15, key=contagem_cobertura_s15.get)
        
        # Pega os elementos que serão cobertos por esta aposta
        elementos_a_remover = {
            sk for sk in itertools.combinations(melhor_aposta, K_SUBGRUPOS_A_COBRIR) 
            if sk in universo_a_cobrir
        }
        
        # 2. Adiciona à solução
        cobertura_final.append(melhor_aposta)

        # 3. ATUALIZAÇÃO: A parte mais inteligente
        for sk_removido in elementos_a_remover:
            # Para cada S15 que também cobria este sk_removido...
            for s15_afetado in mapa_sk_para_s15[sk_removido]:
                # ...sua contagem de cobertura diminui.
                if s15_afetado in contagem_cobertura_s15:
                    contagem_cobertura_s15[s15_afetado] -= 1
        
        # Remove a aposta escolhida do nosso conjunto de candidatos
        del contagem_cobertura_s15[melhor_aposta]
        
        # Remove os elementos efetivamente cobertos do universo
        universo_a_cobrir.difference_update(elementos_a_remover)
        
        # fim_iteracao = time()
        # print(
        #     f"Iteração {iteracao}: "
        #     f"Adicionada aposta. "
        #     f"Cobertos {len(elementos_a_remover)} novos elementos. "
        #     f"Restantes: {len(universo_a_cobrir):,} / {total_elementos_universo:,}. "
        #     f"Solução atual: {len(cobertura_final)} apostas. "
        #     f"Tempo da iteração: {fim_iteracao - inicio_iteracao:.4f}s" # Note o .4f, o tempo será menor
        # )
        iteracao += 1

    # ... (O resto do código para imprimir o resultado final é o mesmo) ...
    # ...
    return cobertura_final


if __name__ == '__main__':
    resolver_cobertura_com_indice_invertido()