from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Calculadora de Aposentadoria funcionando!"}

@app.get("/calcular")
def calcular_aposentadoria(idade: int, contribuicao: int):
    # Exemplo simples de lógica de cálculo
    if idade >= 60 and contribuicao >= 35:
        return {"status": "Aprovado", "mensagem": "Você já pode se aposentar!"}
    return {"status": "Reprovado", "mensagem": "Você ainda não atende aos requisitos para aposentadoria."}
