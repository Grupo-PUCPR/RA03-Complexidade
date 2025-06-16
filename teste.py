from math import comb
import matplotlib.pyplot as plt

ks = [14, 13, 12, 11, 10, 9, 8]
resultados = []

for k in ks:
    valor = comb(25, 15) * (comb(15, k) ** 2)
    print(f'SB({15},{k}) = {valor:,}')
    resultados.append(valor)

plt.figure(figsize=(8, 5))
plt.plot(ks, resultados, marker='o', linestyle='-', color='blue', label='Complexidade estimada')

plt.xlabel(f'Valor de Ka (SB15_Ka)')
plt.ylabel('Complexidade (escala log)')
plt.title('Crescimento da complexidade para diferentes valores de Ka')

plt.yscale('log')  # <<< Adiciona escala logarítmica

plt.text(10, max(resultados)*0.3, r'$\binom{25}{15} \times \left( \binom{15}{K_{a}} \right)^2$', fontsize=14)

plt.gca().invert_xaxis()
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('grafico.png')
plt.show()
