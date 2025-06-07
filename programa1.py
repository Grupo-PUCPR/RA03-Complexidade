from sb import sb_num

for valor in [['a', 15],['b', 14],['c', 13],['d', 12],['e', 11]]:
    sb = sb_num(valor[1])
    print(f"{valor[0]}) Subconjuntos de tamanho {valor[1]}, valores obtidos: {len(sb)}")
