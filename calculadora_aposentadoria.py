import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def formatar_moeda(valor, pos=None):
    """Função auxiliar para formatar valores em SGD"""
    return f'SGD {valor:,.0f}'

def validar_entrada(valor, min_valor, max_valor, nome_campo):
    """Valida os valores de entrada"""
    if not isinstance(valor, (int, float)):
        raise ValueError(f"{nome_campo} deve ser um número")
    if valor < min_valor or valor > max_valor:
        raise ValueError(f"{nome_campo} deve estar entre {min_valor} e {max_valor}")
    return valor

def calcular_aposentadoria(aporte_mensal, anos, taxa_retorno, taxa_retirada):
    """Calcula os valores da aposentadoria"""
    try:
        # Validar entradas
        aporte_mensal = validar_entrada(aporte_mensal, 0, 1000000, "Aporte mensal")
        anos = validar_entrada(anos, 1, 50, "Anos até aposentadoria")
        taxa_retorno = validar_entrada(taxa_retorno, 0.01, 0.20, "Taxa de retorno")
        taxa_retirada = validar_entrada(taxa_retirada, 0.01, 0.10, "Taxa de retirada")
        
        meses = anos * 12
        taxa_mensal = (1 + taxa_retorno) ** (1/12) - 1
        
        saldo_acumulado = [0]
        aportes_totais = [0]
        
        for mes in range(1, meses + 1):
            saldo = saldo_acumulado[-1] * (1 + taxa_mensal) + aporte_mensal
            saldo_acumulado.append(saldo)
            aportes_totais.append(aporte_mensal * mes)
            
        return saldo_acumulado, aportes_totais
    except Exception as e:
        st.error(f"Erro nos cálculos: {str(e)}")
        return None, None

# Configuração da página
st.set_page_config(page_title="Calculadora de Aposentadoria", layout="wide")

# Título e descrição
st.title("Calculadora de Aposentadoria")
st.write("Este aplicativo ajuda você a planejar sua aposentadoria calculando o saque mensal possível com base no aporte mensal e o valor acumulado.")

# Entrada de dados com validação
col1, col2 = st.columns(2)

with col1:
    aporte_mensal = st.number_input(
        "Aporte mensal (SGD):",
        min_value=0.0,
        max_value=1000000.0,
        value=2432.45,
        step=100.0,
        help="Valor mensal que você pretende investir"
    )
    
    anos_ate_aposentadoria = st.slider(
        "Anos até a aposentadoria:",
        min_value=1,
        max_value=50,
        value=25,
        help="Quantidade de anos que você planeja contribuir"
    )

with col2:
    taxa_retorno_anual = st.slider(
        "Taxa de retorno anual (%):",
        min_value=1.0,
        max_value=20.0,
        value=10.0,
        step=0.1,
        help="Rendimento anual esperado dos investimentos"
    ) / 100
    
    taxa_retirada_anual = st.slider(
        "Taxa de retirada anual (%):",
        min_value=1.0,
        max_value=10.0,
        value=4.0,
        step=0.1,
        help="Percentual anual que você pretende retirar na aposentadoria"
    ) / 100

# Cálculos
saldo_acumulado, aportes_totais = calcular_aposentadoria(
    aporte_mensal, 
    anos_ate_aposentadoria, 
    taxa_retorno_anual, 
    taxa_retirada_anual
)

if saldo_acumulado and aportes_totais:
    valor_final = saldo_acumulado[-1]
    total_investido = aportes_totais[-1]
    rendimentos = valor_final - total_investido
    saque_mensal = (valor_final * taxa_retirada_anual) / 12

    # Exibir resultados
    st.subheader("Resultados")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Valor Total Acumulado", f"SGD {valor_final:,.2f}")
    with col2:
        st.metric("Total Investido", f"SGD {total_investido:,.2f}")
    with col3:
        st.metric("Rendimentos", f"SGD {rendimentos:,.2f}")
    
    st.metric("Saque Mensal Possível", f"SGD {saque_mensal:,.2f}")

    # Gerar gráfico
    plt.clf()  # Limpar figura anterior
    fig, ax = plt.subplots(figsize=(12, 6))
    
    meses = np.arange(0, anos_ate_aposentadoria * 12 + 1)
    anos = meses / 12
    
    ax.plot(anos, saldo_acumulado, label="Saldo Acumulado", color="#1f77b4", linewidth=2)
    ax.plot(anos, aportes_totais, label="Total Investido", color="#2ca02c", linewidth=2)
    ax.fill_between(anos, aportes_totais, saldo_acumulado, alpha=0.3, color="#1f77b4", label="Rendimentos")
    
    ax.yaxis.set_major_formatter(FuncFormatter(formatar_moeda))
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title("Evolução do Patrimônio ao Longo do Tempo", pad=20)
    ax.set_xlabel("Anos")
    ax.set_ylabel("Valor (SGD)")
    ax.legend(loc="upper left")
    
    st.pyplot(fig)
    
    # Informações adicionais
    st.subheader("Informações Adicionais")
    st.write(f"""
    - Seu patrimônio será multiplicado por {valor_final/total_investido:.1f}x
    - Os rendimentos representam {(rendimentos/valor_final)*100:.1f}% do valor final
    - O saque mensal representa {(saque_mensal/valor_final)*100:.1f}% do valor final
    """)
