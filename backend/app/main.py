import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from .config import settings
from .routers import auth, profile, roadmap, resources, assessment, resume, recommendations

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Powered Personalized Learning & Career Intelligence Platform API"
)

# Configure CORS for frontend Vite development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all API routers under /api
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(profile.router, prefix=settings.API_V1_STR)
app.include_router(roadmap.router, prefix=settings.API_V1_STR)
app.include_router(resources.router, prefix=settings.API_V1_STR)
app.include_router(assessment.router, prefix=settings.API_V1_STR)
app.include_router(resume.router, prefix=settings.API_V1_STR)
app.include_router(recommendations.router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": "2026-09-18"}

FRONTEND_DIST_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
)
assets_dir = os.path.join(FRONTEND_DIST_DIR, "assets")
os.makedirs(assets_dir, exist_ok=True)
app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

@app.get("/")
async def serve_root():
    index_file = os.path.join(FRONTEND_DIST_DIR, "index.html")
    if os.path.isfile(index_file):
        return FileResponse(index_file)
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "message": "Frontend build not found. Run 'npm run build' inside frontend/ to compile the UI."
    }

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Prevent SPA fallback from masking missing API or Swagger documentation routes
    if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"API route '/{full_path}' not found")

    # Serve static assets directly if they exist in dist (e.g. favicon.svg, icons.svg)
    static_file = os.path.abspath(os.path.join(FRONTEND_DIST_DIR, full_path))
    if static_file.startswith(FRONTEND_DIST_DIR) and os.path.isfile(static_file):
        return FileResponse(static_file)

    # SPA client-side routing fallback (React Router: /dashboard, /roadmap, /assessment, etc.)
    index_file = os.path.join(FRONTEND_DIST_DIR, "index.html")
    if os.path.isfile(index_file):
        return FileResponse(index_file)

    return HTMLResponse("<h1>NovaPath AI</h1><p>Frontend build not found. Run <code>npm run build</code> in <code>frontend/</code>.</p>", status_code=404)

