"""
NovaPath AI - Unified Single URL Server Launcher
------------------------------------------------
Hosts the fullstack platform (React SPA Frontend + FastAPI Backend)
under a single unified URL (default: http://localhost:8000).

Usage:
    python serve.py           # Runs the unified server
    python serve.py --build   # Rebuilds the frontend first, then runs server
    python serve.py --port=8080
"""

import os
import sys
import argparse
import subprocess

def build_frontend():
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "frontend"))
    print(f"📦 Compiling React frontend in {frontend_dir}...")
    result = subprocess.run(["npm", "run", "build"], cwd=frontend_dir, shell=True)
    if result.returncode != 0:
        print("❌ Frontend build failed! Please check npm errors above.")
        sys.exit(result.returncode)
    print("✅ Frontend build completed successfully!\n")

def main():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)

    from app.config import settings

    parser = argparse.ArgumentParser(description="Host NovaPath fullstack website under a single URL")
    parser.add_argument("--port", type=int, default=settings.PORT, help=f"Port to host on (default: {settings.PORT})")
    parser.add_argument("--host", type=str, default=settings.HOST, help=f"Host IP (default: {settings.HOST})")
    parser.add_argument("--build", action="store_true", help="Force rebuild frontend before starting")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    args = parser.parse_args()

    dist_dir = os.path.join(root_dir, "frontend", "dist")

    if args.build or not os.path.isdir(dist_dir) or not os.path.isfile(os.path.join(dist_dir, "index.html")):
        build_frontend()

    import uvicorn

    print("=" * 65)
    print("  NovaPath AI -- Fullstack Single-URL Server Running")
    print(f"  Website URL:       http://localhost:{args.port}")
    print(f"  API Documentation: http://localhost:{args.port}/docs")
    print(f"  API Endpoints:     http://localhost:{args.port}/api")
    print("=" * 65)
    print("Press Ctrl+C to stop the server.\n")

    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=args.reload)

if __name__ == "__main__":
    main()
