from sb import sb_num
from math import comb

for k in [14,13,12,11]:
    formula = comb(25,15) * (comb(15, int(k))**2)
    print(f'O resultado para sb{k} é {formula}')