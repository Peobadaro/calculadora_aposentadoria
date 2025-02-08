from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def homepage(request):
    return JSONResponse({
        "message": "Calculadora de Aposentadoria API",
        "status": "online"
    })

routes = [
    Route("/", endpoint=homepage)
]

app = Starlette(debug=False, routes=routes) 