# NovaPath AI — AI-Powered Personalized Learning & Career Intelligence Platform

A flagship, dark glassmorphic web platform acting as an autonomous student AI academic companion and career mentor. Built for Google Antigravity (agentic IDE).

---

## 🌟 Key Highlights & Architecture

- **Signature 3D "Skill Galaxy" Hero**: Real-time WebGL Three.js canvas featuring 40+ interconnected glowing skill nodes, prerequisite edges, mouse parallax rotation, and node hover inspection cards.
- **Micro-Animated Glassmorphic UI**: Custom cursor ring & dot with magnetic attraction, 3D card tilt physics, gradient text, and fluid Framer Motion page transitions.
- **All 6 Online-Round Hackathon Modules Included**:
  1. **Skill Profiling**: PyMuPDF resume parsing, CV/OCR certificate extraction pipeline, and verified credential tags.
  2. **Adaptive Roadmap Generator**: Topological DAG with Timeline and Graph views, prerequisite enforcement, and milestone clearance with celebratory confetti.
  3. **RAG Resource Recommender**: Vector cosine similarity retrieval over curated engineering topics with provenance grounding rationale.
  4. **Adaptive Assessment Engine**: Dynamic difficulty meter shifting real-time (Easy → Medium → Hard → Expert), code snippet challenges, and grounded conceptual explanations.
  5. **Resume Intelligence & ATS Audit**: Circular ATS score gauge, 3-dimensional breakdown (Skills Match, Quantifiable Metrics, Formatting Health), and 1-click "Add to Roadmap" gap closing.
  6. **AI Opportunities Recommender**: Personalized capstone projects, industry certifications, and internships with explainable "Why this matches your profile" cards.

---

## 🚀 Single-URL Unified Hosting (Recommended)

Run the entire fullstack platform (React SPA + FastAPI APIs + Swagger Docs) under **one single URL**:

```bash
# From the project root:
python serve.py
```
* **Single Website URL**: `http://localhost:8000`
* **API Documentation**: `http://localhost:8000/docs`
* **Backend Endpoints**: `http://localhost:8000/api`

> **Note**: To rebuild the frontend and start in one step, run:
> ```bash
> python serve.py --build
> ```

---

## 🛠️ Separate Development Mode (Optional)

If you prefer hot-reloading frontend and backend independently:

### 1. Start the FastAPI Backend
```bash
cd backend
python -m pip install -r requirements.txt
python run.py
```
*Backend runs at `http://127.0.0.1:8000`.*

### 2. Start the Vite React Frontend
```bash
cd frontend
npm install
npm run dev
```
*Frontend runs at `http://127.0.0.1:5173` (proxies `/api` to port 8000).*

---

## 🐳 Docker Single-URL Deployment

A multi-stage [Dockerfile](file:///Dockerfile) is included to containerize and deploy under a single URL on any cloud host (AWS, Google Cloud Run, Railway, Render, Fly.io):

```bash
docker build -t novapath-ai .
docker run -p 8000:8000 -e PORT=8000 novapath-ai
```

## 🧭 Live Routes & Testing Guide

| Route | Feature Description |
|---|---|
| `/` | Landing page with 3D Skill Galaxy hero, feature showcases, trust stats |
| `/dashboard` | Student intelligence dashboard with Recharts 6-axis radar & trajectory area charts |
| `/roadmap` | Topological DAG curriculum with Timeline/Graph toggles and milestone deep-dive |
| `/assessment` | Adaptive quiz runner with live difficulty adaptation and RAG grounding citation |
| `/resume` | Resume ATS scoring gauge, dimensional breakdown, and skill gap highlighter |
| `/resources` | Grounded study library with real-time semantic search and format filters |
| `/recommendations` | AI-curated capstone projects, certifications, and internships |
| `/onboarding` | 3-step profiling wizard with document upload and OCR simulation |
| `/login` | Authentication with 1-Click "Hackathon Judge Quick-Access" button |
| `/profile` | Student academic records, verified competencies, and trajectory configuration |
