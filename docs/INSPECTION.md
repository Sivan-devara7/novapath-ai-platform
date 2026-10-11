# NovaPath AI Platform — Architectural Inspection Report

**Date:** 2026-10-11  
**Scope:** Phase 0 Inspection of the 10-Feature Upgrade Specification

---

## 1. Feature Classification Matrix (10 Core Features)

Each feature is classified into one of four states:
- **Working**: Fully functional with real backend logic and dynamic data flow.
- **Partial**: Functional heuristic/algorithmic implementation, but lacking dynamic LLM generation or persistent storage.
- **UI-only-mock**: Visual interface present, but operations are simulated with static arrays, timers, or hardcoded constants.
- **Missing**: Not implemented in the codebase.

| # | Feature | Status | Evidence & File Paths | Architectural Gaps & Observations |
|---|---|:---:|---|---|
| **1** | **Previous Learning Recognition** | **UI-only-mock** | [frontend/src/pages/Onboarding.tsx:L38-L58](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/frontend/src/pages/Onboarding.tsx#L38-L58)<br>[backend/app/services/document_service.py](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/backend/app/services/document_service.py) | Frontend uses `setTimeout(..., 1200)` and appends hardcoded skill arrays (`['Transformers', 'Hugging Face', 'Linux']`). The backend has PyMuPDF/regex extraction functions, but the frontend never sends multipart files to `/api/profile/upload-resume`. |
| **2** | **Personalized Learning Roadmap** | **Partial** | [frontend/src/pages/Roadmap.tsx](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/frontend/src/pages/Roadmap.tsx)<br>[backend/app/services/roadmap_service.py:L5-L105](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/backend/app/services/roadmap_service.py#L5-L105) | Frontend renders dual Timeline & Graph views. Backend serves static hardcoded DAG arrays from `CAREER_ROADMAPS` dictionary. Roadmaps are not dynamically generated via LLM based on user profile gaps or saved in a database. |
| **3** | **Intelligent Resource Recommendation** | **Partial** | [frontend/src/pages/Resources.tsx](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/frontend/src/pages/Resources.tsx)<br>[backend/app/services/rag_service.py:L7-L135](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/backend/app/services/rag_service.py#L7-L135) | Keyword/Jaccard search operates over a static in-memory catalog of 8 items (`KNOWLEDGE_BASE`). No live vector embeddings (FAISS/SentenceTransformers) and no dynamic web search or LLM enrichment. |
| **4** | **Resume Analyzer** | **Partial** | [frontend/src/pages/Resume.tsx](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/frontend/src/pages/Resume.tsx)<br>[backend/app/services/ats_service.py:L6-L125](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/backend/app/services/ats_service.py#L6-L125) | Computes ATS score (0-100), metrics counts, and gap detection using rule-based regular expressions against predefined role benchmarks (`ROLE_BENCHMARKS`). Lacks LLM semantic evaluation and personalized bullet-point rewrites. |
| **5** | **Project Recommendation Engine** | **UI-only-mock** | [frontend/src/pages/Recommendations.tsx](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/frontend/src/pages/Recommendations.tsx)<br>[backend/app/routers/recommendations.py:L8-L75](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/backend/app/routers/recommendations.py#L8-L75) | Returns a static array of 6 hardcoded recommendations (`RECOMMENDATIONS_DATABASE`). Does not dynamically match projects to the candidate's actual resume gaps or milestone history. |
| **6** | **Adaptive Assessment** | **Partial** | [frontend/src/pages/Assessment.tsx](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/frontend/src/pages/Assessment.tsx)<br>[backend/app/services/assessment_service.py:L5-L165](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/backend/app/services/assessment_service.py#L5-L165) | Difficulty adjustment logic (Easy -> Medium -> Hard -> Expert based on consecutive correct count) is functional, but draws exclusively from a static bank of 6 questions (`QUESTION_BANK`). Lacks LLM question generation and live code execution. |
| **7** | **Academic & Career Intelligence Assistance** | **UI-only-mock** | [frontend/src/pages/Resume.tsx:L305-L315](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/frontend/src/pages/Resume.tsx#L305-L315)<br>[frontend/src/components/3d/SkillGalaxyHero.tsx](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/frontend/src/components/3d/SkillGalaxyHero.tsx) | No conversational agent or interactive career mentor exists. Academic advice is presented as static summary strings embedded in existing views. |
| **8** | **Progress Tracking & Analytics** | **Partial** | [frontend/src/pages/Dashboard.tsx:L32-L42](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/frontend/src/pages/Dashboard.tsx#L32-L42)<br>[backend/app/routers/auth.py:L7-L25](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/backend/app/routers/auth.py#L7-L25) | Recharts radar and trajectory charts render successfully, but `PROGRESS_HISTORY` is hardcoded. Points and streak exist only in memory on `DEMO_USER` and in browser `localStorage`. |
| **9** | **Offline Learning & Multilingual Support** | **Missing** | N/A | No PWA service worker, no offline sync, and no i18n translation framework configured. |
| **10** | **Learning Style Adaptation** | **Missing** | [frontend/src/pages/Resources.tsx:L44-L52](file:///c:/Users/sivan/OneDrive/Desktop/Websites/Vizag/frontend/src/pages/Resources.tsx#L44-L52) | Content format tabs (`video`, `doc`, `interactive`, `paper`) filter the static catalog, but there is no learning style assessment (e.g. VARK) and no cognitive style adaptation engine. |

---

## 2. Persistence & Database Verification

### Empirical Test Execution
We verified whether `DATABASE_URL` is actively used by the backend:
1. Checked `GET /api/profile/me`: Points returned **`860`**.
2. Mutated state via `POST /api/roadmap/complete-node/py-foundations`: Points increased to **`1160`** in memory.
3. Restarted the backend server process (`python run.py`).
4. Re-queried `GET /api/profile/me`: Points reset back to **`860`**.
5. Checked file system: `novapath.db` does **not** exist (`Exists: False`).

### Conclusion
The backend does **not** currently use an ORM (SQLAlchemy / SQLModel / Tortoise), has no database migrations (Alembic), and does not persist state to SQLite. All data is held in Python memory dictionaries (`DEMO_USER`, `CAREER_ROADMAPS`, `QUESTION_BANK`, `RECOMMENDATIONS_DATABASE`).

---

## 3. Frontend Mock Data Inventory

| Frontend Page | Mock Data Elements |
|---|---|
| **`/` (Landing)** | Hardcoded trust statistics (98.4%, 12,400+ resources, 60 FPS); hardcoded 3D node coordinates in `SkillGalaxyHero.tsx`. |
| **`/dashboard`** | `PROGRESS_HISTORY = [{ week: 'Wk 1', mastery: 35, ats: 58 }, ...]` is hardcoded; default radar competencies are hardcoded in `DEMO_USER`. |
| **`/onboarding`** | Resume and certificate upload routines use `setTimeout(..., 1200)` and hardcoded skill arrays without invoking backend APIs. |
| **`/resources`** | Grounded resources are retrieved from backend, which serves static 8-item dictionary. |
| **`/assessment`** | Questions are retrieved from backend, which serves static 6-item dictionary. |
| **`/resume`** | Defaults to static `SAMPLE_STUDENT_RESUME` string in backend; "Add to Roadmap" only updates component React state. |
| **`/recommendations`** | Displays static 6 recommendations from backend dictionary. |
| **`/login`** | Authenticates against static `DEMO_USER` singleton. |
