import sys
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

# Adiciona o diretório raiz ao PATH do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculadora_aposentadoria import app

# Configuração para o Vercel
if __name__ == "__main__":
    app.run()

async def homepage(request):
    return JSONResponse({
        "message": "Calculadora de Aposentadoria API",
        "status": "online",
        "version": "1.0.0"
    })

async def health_check(request):
    return JSONResponse({
        "status": "healthy"
    })

# Definição das rotas
routes = [
    Route("/", endpoint=homepage),
    Route("/health", endpoint=health_check)
]

# Configuração de middleware com restrições de segurança
middleware = [
    Middleware(
        TrustedHostMiddleware, 
        allowed_hosts=['vercel.app', 'localhost', '127.0.0.1']
    ),
    Middleware(
        CORSMiddleware,
        allow_origins=['https://*.vercel.app', 'http://localhost:*'],
        allow_methods=['GET'],
        allow_headers=['*'],
        allow_credentials=True
    )
]

# Criação da aplicação com configurações de segurança
app = Starlette(
    debug=False,
    routes=routes,
    middleware=middleware
)