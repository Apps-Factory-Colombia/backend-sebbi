from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import questions, pdf, auth, documents
import os

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# Middleware personalizado para manejar OPTIONS requests
@app.middleware("http")
async def cors_handler(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept, Origin, X-Requested-With, Access-Control-Request-Method, Access-Control-Request-Headers"
        response.headers["Access-Control-Max-Age"] = "86400"
        response.status_code = 200
        return response
    
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept, Origin, X-Requested-With, Access-Control-Request-Method, Access-Control-Request-Headers"
    return response

# Configurar CORS - Optimizado para Vercel
# En producción (Vercel), permitir todos los orígenes de forma segura
if os.getenv("VERCEL") == "1" or os.getenv("VERCEL_ENV"):
    # Configuración para Vercel
    origins = [
        "*",  # Permitir todos los orígenes en Vercel
    ]
else:
    # Configuración para desarrollo local
    origins = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "*"  
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Authorization", 
        "Accept",
        "Origin",
        "X-Requested-With",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["*"],
    max_age=86400,  # Cache preflight por 24 horas
)

# Incluir routers
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(questions.router, prefix=settings.API_PREFIX)
app.include_router(pdf.router, prefix=settings.API_PREFIX)
app.include_router(documents.router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {
        "message": f"{settings.APP_NAME} funcionando. Usa los endpoints de {settings.API_PREFIX} para interactuar.",
        "version": settings.VERSION
    }

# Endpoint para verificar CORS
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "cors": "enabled",
        "environment": "vercel" if os.getenv("VERCEL") else "local"
    }

# Manejar todas las solicitudes OPTIONS explícitamente
@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept, Origin, X-Requested-With, Access-Control-Request-Method, Access-Control-Request-Headers",
            "Access-Control-Max-Age": "86400"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
