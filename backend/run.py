import os
import uvicorn

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "false").lower() in ("true", "1")
    print(f"NovaPath AI Unified Server starting at http://localhost:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)

