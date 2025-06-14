import itertools
from time import time
from math import comb

# --- PARÂMETROS GERAIS DO PROBLEMA ---
# Altere este valor para resolver para S14, S13, S12 ou S11 (Programas 2 a 5)
K_SUBGRUPOS_A_COBRIR = 14  # Exemplo: 14 para o PROGRAMA 2 (cobrir S14)

UNIVERSO_TOTAL = set(range(1, 26))
N_UNIVERSO = 25
K_APOSTA_S15 = 15
CUSTO_POR_APOSTA = 3.00


def resolver_cobertura_de_conjuntos_sequencial():
    """
    Função principal que implementa o algoritmo guloso de forma SEQUENCIAL.
    """
    # Tarefa 1 (Geração de Combinações): O universo Sk é gerado e armazenado em um set.
    print(f"--- Iniciando a resolução para k={K_SUBGRUPOS_A_COBRIR} ---")
    print("PROGRAMA 1: Gerando o universo de combinações a serem cobertas (Sk)...")
    
    universo_a_cobrir = {
        comb 
        for comb in itertools.combinations(UNIVERSO_TOTAL, K_SUBGRUPOS_A_COBRIR)
    }
    total_elementos_universo = len(universo_a_cobrir)
    print(f"Universo Sk (k={K_SUBGRUPOS_A_COBRIR}) gerado com {total_elementos_universo:,} combinações.")
    print("-" * 50)
    print("AVISO: Executando em modo SEQUENCIAL (single-core).")
    print("Esta execução será EXTREMAMENTE LENTA e pode levar muitas horas ou dias.")
    print("-" * 50)


    # PROGRAMAS 2-5: Implementação do algoritmo guloso
    cobertura_final = []
    
    iteracao = 1
    while universo_a_cobrir:
        inicio_iteracao = time()
        
        # Variáveis para encontrar a melhor aposta da iteração atual
        melhor_aposta_iteracao = None
        elementos_cobertos_pela_melhor = set()
        max_cobertos = -1

        # ALTERAÇÃO PRINCIPAL: Laço 'for' sequencial que substitui o multiprocessing.
        # Este laço itera sobre TODAS as 3.2 milhões de apostas S15 candidatas.
        # Esta é a etapa mais demorada do programa.
        for aposta_s15 in itertools.combinations(UNIVERSO_TOTAL, K_APOSTA_S15):
            
            # Gera todas as combinações Sk que esta aposta S15 cobre
            subgrupos_cobertos_pela_aposta = set(itertools.combinations(aposta_s15, K_SUBGRUPOS_A_COBRIR))
            
            # Calcula a interseção com os elementos que ainda faltam cobrir
            novos_elementos_cobertos = universo_a_cobrir.intersection(subgrupos_cobertos_pela_aposta)
            
            # Se encontrou uma aposta melhor que a anterior, atualiza.
            if len(novos_elementos_cobertos) > max_cobertos:
                max_cobertos = len(novos_elementos_cobertos)
                melhor_aposta_iteracao = aposta_s15
                elementos_cobertos_pela_melhor = novos_elementos_cobertos

        # Se encontrou uma aposta que cobre novos elementos, atualiza o estado
        if melhor_aposta_iteracao:
            cobertura_final.append(melhor_aposta_iteracao)
            universo_a_cobrir.difference_update(elementos_cobertos_pela_melhor)
        else:
            # Condição de parada caso não encontre mais apostas que cubram algo novo
            print("Nenhuma aposta consegue cobrir os elementos restantes. Finalizando.")
            break

        fim_iteracao = time()
        
        # Relatório de progresso
        print(
            f"Iteração {iteracao}: "
            f"Adicionada aposta {melhor_aposta_iteracao}. "
            f"Cobertos {max_cobertos} novos elementos. "
            f"Restantes: {len(universo_a_cobrir):,} / {total_elementos_universo:,}. "
            f"Solução atual: {len(cobertura_final)} apostas. "
            f"Tempo da iteração: {fim_iteracao - inicio_iteracao:.2f}s"
        )
        iteracao += 1

    print("\n" + "="*50)
    print("Cobertura de Conjuntos Finalizada!")
    print(f"O menor subconjunto encontrado (SB15_{K_SUBGRUPOS_A_COBRIR}) contém {len(cobertura_final)} apostas.")

    # Tarefa 7: Cálculo do custo financeiro
    custo_total = len(cobertura_final) * CUSTO_POR_APOSTA
    print(f"\nTAREFA 7: CÁLCULO FINANCEIRO")
    print(f"Custo por aposta: R$ {CUSTO_POR_APOSTA:.2f}")
    print(f"Custo total para as {len(cobertura_final)} apostas: R$ {custo_total:,.2f}")
    print("="*50)
    
    return cobertura_final


if __name__ == "__main__":
    
    # Análise de Complexidade (Tarefa 6) - ATUALIZADA PARA VERSÃO SEQUENCIAL
    print("TAREFA 6: ANÁLISE DE COMPLEXIDADE (Algoritmo Guloso Sequencial)")
    print("Parâmetros:")
    print(f"  N = {N_UNIVERSO} (números totais)")
    print(f"  M = C({N_UNIVERSO}, {K_APOSTA_S15}) = {comb(N_UNIVERSO, K_APOSTA_S15):,} (total de apostas S15 possíveis)")
    print(f"  |U_k| = C({N_UNIVERSO}, {K_SUBGRUPOS_A_COBRIR}) = {comb(N_UNIVERSO, K_SUBGRUPOS_A_COBRIR):,} (tamanho do universo Sk a cobrir)")
    print(f"  C_k = Tamanho da solução final (a ser encontrada)")
    
    print("\nComplexidade de Tempo (Pior Caso):")
    print(f"  - Por iteração (busca pela melhor aposta): O( M * C({K_APOSTA_S15}, {K_SUBGRUPOS_A_COBRIR}) * k )")
    print(f"    - M: O algoritmo avalia todas as M apostas candidatas.")
    print(f"    - C({K_APOSTA_S15}, {K_SUBGRUPOS_A_COBRIR})): Para cada aposta S15, gera os Sk que ela cobre.")
    print(f"    - k: Custo para hashear/comparar cada combinação Sk.")
    print(f"  - Total: O( C_k * M * C({K_APOSTA_S15}, {K_SUBGRUPOS_A_COBRIR}) * k )")
    print("  Sem paralelismo, o tempo de busca em cada iteração é diretamente proporcional ao número total M de apostas S15.")

    print("\nComplexidade de Espaço:")
    print(f"  - O( |U_k| * k ): Para armazenar o conjunto de elementos Sk a serem cobertos na memória principal.")
    print("-" * 50)
    
    # Execução do programa
    solucao_encontrada = resolver_cobertura_de_conjuntos_sequencial()