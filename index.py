from fastapi import FastAPI
from calculadora_aposentadoria import calcular_aposentadoria  # Importe a função ou lógica do arquivo

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Calculadora de Aposentadoria funcionando!"}

@app.get("/calcular")
def calcular(idade: int, contribuicao: int):
    # Utilize a função do arquivo calculadora_aposentadoria.py
    resultado = calcular_aposentadoria(idade, contribuicao)
    return resultado
