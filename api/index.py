import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from calculadora_aposentadoria import app

# Função para servir a aplicação
def handler(request, response):
    return app(request, response) 