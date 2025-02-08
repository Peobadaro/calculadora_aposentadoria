from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="Calculadora de Aposentadoria API")

class AposentadoriaRequest(BaseModel):
    aporte_mensal: float
    anos: int
    taxa_retorno: float
    taxa_retirada: float

class AposentadoriaResponse(BaseModel):
    valor_final: float
    total_investido: float
    rendimentos: float
    saque_mensal: float
    saldo_acumulado: list[float]
    aportes_totais: list[float]

def validar_entrada(valor, min_valor, max_valor, nome_campo):
    """Valida os valores de entrada"""
    if not isinstance(valor, (int, float)):
        raise ValueError(f"{nome_campo} deve ser um número")
    if valor < min_valor or valor > max_valor:
        raise ValueError(f"{nome_campo} deve estar entre {min_valor} e {max_valor}")
    return valor

def calcular_aposentadoria(aporte_mensal: float, anos: int, taxa_retorno: float, taxa_retirada: float):
    """Calcula os valores da aposentadoria"""
    try:
        meses = anos * 12
        taxa_mensal = (1 + taxa_retorno) ** (1/12) - 1
        
        saldo_acumulado = [0]
        aportes_totais = [0]
        
        for mes in range(1, meses + 1):
            saldo = saldo_acumulado[-1] * (1 + taxa_mensal) + aporte_mensal
            saldo_acumulado.append(saldo)
            aportes_totais.append(aporte_mensal * mes)
        
        valor_final = saldo_acumulado[-1]
        total_investido = aportes_totais[-1]
        rendimentos = valor_final - total_investido
        saque_mensal = (valor_final * taxa_retirada) / 12
        
        return {
            "valor_final": valor_final,
            "total_investido": total_investido,
            "rendimentos": rendimentos,
            "saque_mensal": saque_mensal,
            "saldo_acumulado": saldo_acumulado,
            "aportes_totais": aportes_totais
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    """Endpoint raiz com informações básicas da API"""
    return {
        "message": "Calculadora de Aposentadoria API",
        "version": "1.0.0",
        "endpoints": {
            "/": "Informações da API",
            "/docs": "Documentação OpenAPI",
            "/calcular": "Calcular aposentadoria (POST)"
        }
    }

@app.post("/calcular", response_model=AposentadoriaResponse)
async def calcular(request: AposentadoriaRequest):
    """Calcula os valores da aposentadoria com base nos parâmetros fornecidos"""
    try:
        # Validar entradas
        aporte_mensal = validar_entrada(request.aporte_mensal, 0, 1000000, "Aporte mensal")
        anos = validar_entrada(request.anos, 1, 50, "Anos até aposentadoria")
        taxa_retorno = validar_entrada(request.taxa_retorno, 0.01, 0.20, "Taxa de retorno")
        taxa_retirada = validar_entrada(request.taxa_retirada, 0.01, 0.10, "Taxa de retirada")
        
        # Calcular resultados
        resultados = calcular_aposentadoria(
            aporte_mensal=aporte_mensal,
            anos=anos,
            taxa_retorno=taxa_retorno,
            taxa_retirada=taxa_retirada
        )
        
        return resultados
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
