import os
import uvicorn
from app.config import settings

if __name__ == "__main__":
    host = settings.HOST
    port = settings.PORT
    reload = os.getenv("RELOAD", "false").lower() in ("true", "1")
    print(f"NovaPath AI Backend Server starting at http://localhost:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)
