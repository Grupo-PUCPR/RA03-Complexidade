import itertools
import multiprocessing
from time import time
from math import comb
from collections import defaultdict
import os
import pickle  # Usaremos para salvar e carregar os dados nos arquivos
import tempfile # Para gerenciar arquivos temporários de forma segura


# Comentarios gemini para entender, mas basicamente indexa subgrupos -> grupos de numeros que sao englobados
# multithread
# alto custo de processamenteo e memoria RAM

# --- PARÂMETROS GERAIS DO PROBLEMA ---
# Altere este valor para resolver para S14, S13, S12 ou S11 (Programas 2 a 5)

# --- Suas constantes permanecem as mesmas ---
K_ALVO = 11
UNIVERSO_TOTAL = range(1, 26)
N_UNIVERSO = 25
K_APOSTA = 15
CUSTO_POR_APOSTA = 3.00

# --- NOVAS FUNÇÕES PARA SUBSTITUIR ---

def construir_indice_parcial_em_disco(lote_de_apostas, nome_arquivo_saida):
    """
    NOVA FUNÇÃO WORKER:
    Cria um pedaço do índice e o salva diretamente em um arquivo no disco,
    em vez de retorná-lo pela memória.
    """
    mapa_parcial = defaultdict(list)
    for aposta_s15 in lote_de_apostas:
        for alvo_sk in itertools.combinations(aposta_s15, K_ALVO):
            mapa_parcial[alvo_sk].append(aposta_s15)
    
    # Usa o módulo 'pickle' para serializar e salvar o dicionário no arquivo.
    with open(nome_arquivo_saida, 'wb') as f:
        pickle.dump(mapa_parcial, f)
    
    return nome_arquivo_saida # Retorna apenas o nome do arquivo criado

def construir_indice_invertido_paralelo_com_disco():
    """
    NOVO ORQUESTRADOR:
    Gerencia os workers para que salvem os resultados em disco e depois
    junta os resultados lendo os arquivos um a um.
    """
    # Mesmo com muita RAM, é prudente limitar os processos para evitar sobrecarga geral.
    num_processos = max(1, os.cpu_count() - 2) if os.cpu_count() else 1
    print(f"ETAPA 1: Construindo Índice com {num_processos} processos (MODO SEGURO DE MEMÓRIA - DISCO)...")

    apostas_s15_gen = itertools.combinations(UNIVERSO_TOTAL, K_APOSTA)
    
    total_apostas = comb(N_UNIVERSO, K_APOSTA)
    print(f"Total de apostas: {total_apostas}")
    tamanho_lote = (total_apostas // num_processos) + 1
    
    # Prepara os argumentos para cada processo: o lote de dados e um nome de arquivo único.
    argumentos_pool = []
    lote_atual = []
    processo_id = 0
    
    # Cria um diretório temporário para nossos arquivos de índice
    diretorio_temporario = tempfile.mkdtemp()
    print(f"   ... Arquivos de índice temporários serão salvos em: {diretorio_temporario}")

    for aposta in apostas_s15_gen:
        lote_atual.append(aposta)
        if len(lote_atual) == tamanho_lote:
            nome_arquivo = os.path.join(diretorio_temporario, f"indice_parcial_{processo_id}.pkl")
            argumentos_pool.append((lote_atual, nome_arquivo))
            lote_atual = []
            processo_id += 1
    if lote_atual:
        nome_arquivo = os.path.join(diretorio_temporario, f"indice_parcial_{processo_id}.pkl")
        argumentos_pool.append((lote_atual, nome_arquivo))

    # Inicia o processamento paralelo
    with multiprocessing.Pool(processes=num_processos) as pool:
        # starmap é usado quando a função worker tem múltiplos argumentos
        nomes_arquivos_criados = pool.starmap(construir_indice_parcial_em_disco, argumentos_pool)

    print(f"   ... {len(nomes_arquivos_criados)} arquivos de índice parciais foram criados.")
    print("   ... Juntando os resultados a partir dos arquivos (isso pode levar um tempo)...")

    # Junta os resultados LENDO UM ARQUIVO DE CADA VEZ
    mapa_sk_para_s15 = defaultdict(list)
    for nome_arquivo in nomes_arquivos_criados:
        with open(nome_arquivo, 'rb') as f:
            mapa_parcial = pickle.load(f)
            for sk, lista_s15 in mapa_parcial.items():
                mapa_sk_para_s15[sk].extend(lista_s15)
        # Remove o arquivo temporário após o uso para economizar espaço em disco
        os.remove(nome_arquivo)
    
    # Remove o diretório temporário
    os.rmdir(diretorio_temporario)

    return mapa_sk_para_s15

def resolver_com_guloso_otimizado():
    """
    A implementação completa e otimizada do algoritmo guloso.
    """
    inicio_total = time()

    # ETAPA 1: Construção do Índice
    mapa_sk_para_s15 = construir_indice_invertido_paralelo_com_disco()
    print(f"Índice construído em {time() - inicio_total:.2f}s.\n")

    # ETAPA 2: Preparação das estruturas de dados do loop
    print("ETAPA 2: Preparando estruturas para o loop guloso (Buckets)...")
    
    universo_a_cobrir = set(mapa_sk_para_s15.keys())
    total_alvos = len(universo_a_cobrir)
    
    # Estrutura de "Buckets" para acesso O(1) à melhor aposta
    # `buckets[i]` conterá um `set` de todas as apostas que atualmente cobrem `i` alvos.
    pontuacao_maxima = comb(K_APOSTA, K_ALVO)
    buckets = [set() for _ in range(pontuacao_maxima + 1)]
    
    # Mapa para rastrear a pontuação atual de cada aposta
    mapa_s15_para_pontuacao = {}
    
    apostas_s15_todas = list(itertools.combinations(UNIVERSO_TOTAL, K_APOSTA))
    for aposta in apostas_s15_todas:
        # No início, todas as apostas têm a pontuação máxima
        buckets[pontuacao_maxima].add(aposta)
        mapa_s15_para_pontuacao[aposta] = pontuacao_maxima
    
    print("Estruturas prontas.\n")

    # ETAPA 3: Loop Guloso Otimizado com Buckets
    print("Cobrindo o universo", total_alvos)
    print("ETAPA 3: Iniciando o Loop Guloso Otimizado...")
    
    cobertura_final = []
    pontuacao_atual = pontuacao_maxima
    iteracao = 1

    while universo_a_cobrir:
        
        # Encontra o bucket de maior pontuação que não está vazio
        while not buckets[pontuacao_atual]:
            pontuacao_atual -= 1
        
        # Pega qualquer aposta desse bucket (todas são igualmente "boas" neste passo)
        melhor_aposta = buckets[pontuacao_atual].pop()
        cobertura_final.append(melhor_aposta)

        # Identifica os alvos que esta aposta cobre e que ainda não estavam na cobertura
        alvos_cobertos_nesta_rodada = {
            sk for sk in itertools.combinations(melhor_aposta, K_ALVO) if sk in universo_a_cobrir
        }

        # Atualiza as pontuações de outras apostas que foram afetadas
        for alvo_coberto in alvos_cobertos_nesta_rodada:
            # Para cada S15 que também cobria este alvo...
            for aposta_afetada in mapa_sk_para_s15[alvo_coberto]:
                # Se a aposta afetada ainda está em jogo...
                if aposta_afetada in mapa_s15_para_pontuacao:
                    # ...move ela para um bucket de pontuação inferior.
                    pontuacao_antiga = mapa_s15_para_pontuacao[aposta_afetada]
                    buckets[pontuacao_antiga].discard(aposta_afetada)
                    
                    nova_pontuacao = pontuacao_antiga - 1
                    buckets[nova_pontuacao].add(aposta_afetada)
                    mapa_s15_para_pontuacao[aposta_afetada] = nova_pontuacao
        
        # Remove os alvos recém-cobertos do universo
        universo_a_cobrir.difference_update(alvos_cobertos_nesta_rodada)
        del mapa_s15_para_pontuacao[melhor_aposta] # Remove a aposta escolhida do jogo
    
        iteracao += 1

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


if __name__ == '__main__':
    for i in resolver_com_guloso_otimizado():
        print(i)