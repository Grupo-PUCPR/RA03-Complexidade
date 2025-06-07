from sb import sb_num
import random

sb15 = sb_num(15)
sb14 = sb_num(14)
#print(sb15, '\n', sb14) 

subconjunto = []
sb15_copy = sb15.copy()
sb14_copy = sb14.copy()  

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
def combina_com_outras_repetida(comb, combinacoes, limiar_similaridade=0.8):
    combincao = set(comb)
    for c in combinacoes:
        comb_c = set(c)
        intersecao = len(combincao.intersection(comb_c))
        similaridade = intersecao / len(combincao)
        if similaridade >= limiar_similaridade:
            return True
    return False

#Funciona, mas a complexidade é muito alta

for _ in sb15:
    combinacao = random.choice(sb15_copy)
    #se a combinação tem sequência, remove e continua
    if tem_sequencia_longa(combinacao):
        sb15_copy.remove(combinacao)
        continue

    #se a combinação tem alta sobreposição com alguma combinação da lista, remove e continua
    if combina_com_outras_repetida(combinacao, sb14_copy):
        sb15_copy.remove(combinacao)
        continue

    set_combinacao = set(combinacao) # faço um set (coleção de itens únicos)
    remover = []  
    for comb2 in sb14_copy:
        set_comb2 = set(comb2)
        #se minha comb menor tem na combinação maior
        if set_comb2.issubset(set_combinacao):
            remover.append(comb2)
    
    #remove cada item do meu sb2
    for item in remover:
        sb14_copy.remove(item)

    #só add a combinação a solução se eu tiver itens para remover
    if remover: 
        subconjunto.append(combinacao)

print("Subconjuntos escolhidos:", len(subconjunto))