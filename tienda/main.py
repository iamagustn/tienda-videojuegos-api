from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tienda.rutas.productos as productos
import tienda.rutas.cuentas as cuentas
import logging
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    force=True
)

logger = logging.getLogger(__name__)

app = FastAPI()

origins =[  
    "http://localhost:5173",
]

@app.exception_handler(RequestValidationError)
def manejar_validacion(request, exc):
    mi_lista = []
    for error in exc.errors():
        loc = error["loc"]
        msg = error["msg"]
        if "body" in loc:
            mi_lista.append(f"Error en el campo {loc[-1]}: {msg}")
        else:
            mi_lista.append("El identificador debe ser un número entero")

    return JSONResponse(status_code=422, content={"detail": " | ".join(mi_lista)})

@app.exception_handler(Exception)
def manejar_error_server(request, exc):
    clave = str(uuid.uuid4())
    logger.error("Ocurrio un error interno en el servidor: con la clave %s", clave, exc_info=exc)
    return JSONResponse(status_code=500, content={
        "detail": "Ocurrio un error interno en el servidor. Trabajaremos para mejorar el sistema.",
        "id_error": clave
    })

app.include_router(productos.router)
app.include_router(cuentas.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
