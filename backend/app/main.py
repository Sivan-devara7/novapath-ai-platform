from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import settings, log_startup_config
from .core.database import init_db
from .routers import (
    auth,
    profile,
    roadmap,
    resources,
    assessment,
    resume,
    recommendations,
    modules,
    mentor,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Powered Personalized Learning & Career Intelligence Platform API",
)


@app.on_event("startup")
async def startup_event():
    log_startup_config()
    init_db()


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(profile.router, prefix=settings.API_V1_STR)
app.include_router(roadmap.router, prefix=settings.API_V1_STR)
app.include_router(modules.router, prefix=settings.API_V1_STR)
app.include_router(resources.router, prefix=settings.API_V1_STR)
app.include_router(assessment.router, prefix=settings.API_V1_STR)
app.include_router(resume.router, prefix=settings.API_V1_STR)
app.include_router(recommendations.router, prefix=settings.API_V1_STR)
app.include_router(mentor.router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "health": "/health",
        "docs": "/docs",
        "ai_health": "/api/ai/health",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "NovaPath AI Backend",
    }


@app.get("/api/ai/health")
async def ai_health():
    """Check whether OmniRoute can complete a real AI request."""

    if not settings.is_ai_available:
        return {
            "ok": False,
            "reason": "OMNIROUTE_API_KEY is not configured",
        }

    import time
    import httpx

    try:
        url = (
            f"{settings.OMNIROUTE_BASE_URL.rstrip('/')}"
            "/chat/completions"
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.OMNIROUTE_API_KEY}",
        }

        payload = {
            "model": settings.OMNIROUTE_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": "Reply with the word OK",
                }
            ],
            "max_tokens": 10,
        }

        start = time.perf_counter()

        timeout_seconds = min(
            float(settings.OMNIROUTE_TIMEOUT_SECONDS),
            25.0,
        )

        async with httpx.AsyncClient(
            timeout=timeout_seconds
        ) as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers,
            )

        latency_ms = round(
            (time.perf_counter() - start) * 1000
        )

        if response.status_code != 200:
            return {
                "ok": False,
                "reason": (
                    "OmniRoute returned HTTP "
                    f"{response.status_code}"
                ),
            }

        data = response.json()

        reply = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        return {
            "ok": True,
            "model": settings.OMNIROUTE_MODEL,
            "latency_ms": latency_ms,
            "test_response": reply,
        }

    except httpx.TimeoutException:
        return {
            "ok": False,
            "reason": "OmniRoute request timed out",
        }

    except httpx.RequestError:
        return {
            "ok": False,
            "reason": "Could not connect to OmniRoute",
        }

    except Exception as exc:
        return {
            "ok": False,
            "reason": type(exc).__name__,
        }


@app.get("/{full_path:path}")
async def not_found(full_path: str):
    raise HTTPException(
        status_code=404,
        detail=f"API endpoint '/{full_path}' not found",
    )
