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

# Configurar CORS primero - Optimizado para Vercel
origins = ["*"]

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
    max_age=86400,
)

# Middleware personalizado para manejar OPTIONS requests y agregar headers CORS
@app.middleware("http")
async def cors_handler(request: Request, call_next):
    # Manejar preflight OPTIONS requests
    if request.method == "OPTIONS":
        response = Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept, Origin, X-Requested-With, Access-Control-Request-Method, Access-Control-Request-Headers"
        response.headers["Access-Control-Max-Age"] = "86400"
        response.status_code = 200
        return response
    
    # Procesar request normal
    response = await call_next(request)
    
    # Agregar headers CORS a todas las respuestas
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept, Origin, X-Requested-With, Access-Control-Request-Method, Access-Control-Request-Headers"
    
    return response

# Incluir routers
app.include_router(documents.router, prefix=settings.API_PREFIX)
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(questions.router, prefix=settings.API_PREFIX)
app.include_router(pdf.router, prefix=settings.API_PREFIX)

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

# Endpoint para debug de rutas
@app.get("/debug/routes")
async def debug_routes():
    routes_info = []
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            routes_info.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": getattr(route, 'name', 'unknown')
            })
    return {
        "total_routes": len(routes_info),
        "routes": routes_info
    }

# Endpoint específico para debug de documents
@app.get("/debug/documents")
async def debug_documents():
    return {
        "endpoint": "/api/v1/documents",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "status": "active",
        "cors": "enabled",
        "router_routes": len(documents.router.routes)
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
