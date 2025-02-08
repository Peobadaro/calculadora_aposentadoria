import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Função para calcular o saldo acumulado e o aporte mensal necessário
def calcular_aposentadoria(saque_desejado, anos_ate_aposentadoria, taxa_retorno_anual, taxa_retirada_anual):
    meses = anos_ate_aposentadoria * 12
    taxa_mensal = (1 + taxa_retorno_anual) ** (1 / 12) - 1

    # Valor necessário na aposentadoria
    valor_necessario = (saque_desejado * 12) / taxa_retirada_anual

    # Aporte mensal necessário
    aporte_mensal = valor_necessario / (((1 + taxa_mensal) ** meses - 1) / taxa_mensal)

    # Saldo acumulado ao longo do tempo
    saldo_acumulado = [0]
    for mes in range(1, meses + 1):
        saldo = saldo_acumulado[-1] * (1 + taxa_mensal) + aporte_mensal
        saldo_acumulado.append(saldo)

    return valor_necessario, aporte_mensal, saldo_acumulado

# Parâmetros personalizados pelo usuário
print("=== Planejamento de Aposentadoria ===")
saque_desejado = float(input("Digite o saque mensal desejado (SGD): "))
anos_ate_aposentadoria = int(input("Digite o número de anos até a aposentadoria: "))
taxa_retorno_anual = float(input("Digite a taxa de retorno anual (%): ")) / 100
taxa_retirada_anual = 0.04  # Regra dos 4%

# Cálculos
valor_necessario, aporte_mensal, saldo_acumulado = calcular_aposentadoria(
    saque_desejado, anos_ate_aposentadoria, taxa_retorno_anual, taxa_retirada_anual
)

# Exibir resultados
print("\n=== Resultados ===")
print(f"Saque Mensal Desejado: SGD {saque_desejado:,.2f}")
print(f"Valor Necessário na Aposentadoria: SGD {valor_necessario:,.2f}")
print(f"Aporte Mensal Necessário: SGD {aporte_mensal:,.2f}")

# Gerar gráfico do saldo acumulado
meses = np.arange(0, anos_ate_aposentadoria * 12 + 1)
plt.figure(figsize=(10, 6))
plt.plot(meses, saldo_acumulado, label="Saldo Acumulado", linewidth=2)
plt.axhline(y=valor_necessario, color='r', linestyle='--', label="Valor Necessário")
plt.title("Crescimento do Saldo Acumulado para Aposentadoria")
plt.xlabel("Meses")
plt.ylabel("Saldo Acumulado (SGD)")
plt.legend()
plt.grid()
plt.show()
