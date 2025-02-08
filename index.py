from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def homepage():
    return JSONResponse({
        "message": "Calculadora de Aposentadoria API",
        "status": "online"
    }) 