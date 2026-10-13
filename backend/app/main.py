import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from .config import settings, log_startup_config
from .core.database import init_db
from .routers import auth, profile, roadmap, resources, assessment, resume, recommendations, modules, mentor

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Powered Personalized Learning & Career Intelligence Platform API"
)

@app.on_event("startup")
async def startup_event():
    log_startup_config()
    init_db()

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
app.include_router(modules.router, prefix=settings.API_V1_STR)
app.include_router(resources.router, prefix=settings.API_V1_STR)
app.include_router(assessment.router, prefix=settings.API_V1_STR)
app.include_router(resume.router, prefix=settings.API_V1_STR)
app.include_router(recommendations.router, prefix=settings.API_V1_STR)
app.include_router(mentor.router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": "2026-09-18",
    }

@app.get("/api/ai/health")
async def ai_health():
    """Checks OmniRoute AI availability with a real completion call. Never exposes keys."""
    if not settings.is_ai_available:
        return {"ok": False, "reason": "OMNIROUTE_API_KEY not set"}

    import time
    import httpx
    try:
        url = f"{settings.OMNIROUTE_BASE_URL.rstrip('/')}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.OMNIROUTE_API_KEY}"
        }
        payload = {
            "model": settings.OMNIROUTE_MODEL,
            "messages": [{"role": "user", "content": "Reply with the word OK"}],
            "max_tokens": 10
        }
        start = time.perf_counter()
        timeout_sec = min(float(settings.OMNIROUTE_TIMEOUT_SECONDS), 25.0)
        async with httpx.AsyncClient(timeout=timeout_sec) as client:
            res = await client.post(url, json=payload, headers=headers)
            latency_ms = round((time.perf_counter() - start) * 1000)
            if res.status_code == 200:
                data = res.json()
                reply = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                return {
                    "ok": True,
                    "model": settings.OMNIROUTE_MODEL,
                    "latency_ms": latency_ms,
                    "test_response": reply
                }
            else:
                return {"ok": False, "reason": f"OmniRoute responded with HTTP {res.status_code}"}
    except Exception as exc:
        return {"ok": False, "reason": f"OmniRoute connection failed: {type(exc).__name__}"}

# Frontend build directory.
# On Vercel, the frontend may be deployed separately.
FRONTEND_DIST_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "frontend",
        "dist",
    )
)

assets_dir = os.path.join(FRONTEND_DIST_DIR, "assets")

# Never create directories during application startup on Vercel.
# Mount assets only when the directory already exists.
if os.path.isdir(assets_dir):
    app.mount(
        "/assets",
        StaticFiles(directory=assets_dir),
        name="assets",
    )


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
        "message": (
            "Backend is running. "
            "The frontend is deployed separately or its build is unavailable."
        ),
    }


@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Do not let the frontend fallback intercept API or documentation routes.
    if (
        full_path == "api"
        or full_path.startswith("api/")
        or full_path == "docs"
        or full_path.startswith("docs/")
        or full_path == "openapi.json"
    ):
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail=f"API route '/{full_path}' not found",
        )

    # Serve a static file only if the frontend build contains it.
    requested_file = os.path.abspath(
        os.path.join(FRONTEND_DIST_DIR, full_path)
    )

    if (
        requested_file.startswith(FRONTEND_DIST_DIR + os.sep)
        and os.path.isfile(requested_file)
    ):
        return FileResponse(requested_file)

    # React Router fallback.
    index_file = os.path.join(FRONTEND_DIST_DIR, "index.html")

    if os.path.isfile(index_file):
        return FileResponse(index_file)

    return HTMLResponse(
        """
        <h1>NovaPath AI Backend</h1>
        <p>The backend is running, but the frontend is not available here.</p>
        <p>Visit <a href="/docs">API Documentation</a> to inspect the API.</p>
        """,
        status_code=200,
    )
