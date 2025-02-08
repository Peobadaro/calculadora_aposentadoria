import streamlit as st
import sys
import os

# Adiciona o diretório raiz ao PATH do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa e executa a aplicação
import calculadora_aposentadoria

if __name__ == "__main__":
    calculadora_aposentadoria.app.run() 