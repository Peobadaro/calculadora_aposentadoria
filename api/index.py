import sys
import os

# Adiciona o diretório raiz ao PATH do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculadora_aposentadoria import app

# Configuração para o Vercel
if __name__ == "__main__":
    app.run()