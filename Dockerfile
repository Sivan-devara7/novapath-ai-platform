# Multi-stage Dockerfile for NovaPath AI Fullstack Single-URL Deployment

# Stage 1: Build the React SPA Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Production Python Backend + Static Hosting
FROM python:3.11-slim AS production
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    HOST=0.0.0.0

# Install dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend assets from stage 1 into frontend/dist
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Copy unified serve script
COPY serve.py ./

EXPOSE 8000

WORKDIR /app/backend
CMD ["python", "run.py"]
