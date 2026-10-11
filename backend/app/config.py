import os
import logging
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

logger = logging.getLogger("novapath.config")

# Resolve backend directory regardless of the current working directory
_backend_dir = Path(__file__).resolve().parent.parent
_env_file = _backend_dir / ".env"
_root_env = _backend_dir.parent / ".env"

# Load backend/.env with override=False so real environment variables ALWAYS win
if _env_file.is_file():
    load_dotenv(dotenv_path=_env_file, override=False)
elif _root_env.is_file():
    load_dotenv(dotenv_path=_root_env, override=False)
else:
    load_dotenv(override=False)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_env_file) if _env_file.is_file() else None,
        env_file_encoding="utf-8",
        extra="ignore"
    )

    PROJECT_NAME: str = "AI Learning & Career Intelligence Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # OmniRoute & AI Settings
    OMNIROUTE_BASE_URL: str = "http://127.0.0.1:20128/v1"
    OMNIROUTE_API_KEY: str = ""
    OMNIROUTE_MODEL: str = "auto"
    OMNIROUTE_FAST_MODEL: str = ""
    OMNIROUTE_STRONG_MODEL: str = ""
    OMNIROUTE_TIMEOUT_SECONDS: int = 60

    # Dedicated Chatbox / Mentor Key (used only for chatbox, isolates other APIs)
    CHATBOX_API_KEY: str = "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"
    CHATBOX_MODEL: str = "openai/gpt-4o-mini"
    CHATBOX_BASE_URL: str = "https://openrouter.ai/api/v1"

    # Auth & Database
    JWT_SECRET: str = "change-me"
    SECRET_KEY: Optional[str] = None
    DATABASE_URL: str = ""

    # Placement Quiz Config (Requirements Update v2 - Section A)
    PLACEMENT_BEGINNER_MAX_RATIO: float = 0.39   # < 40%
    PLACEMENT_INTERMEDIATE_MAX_RATIO: float = 0.74 # 40% - 74%
    PLACEMENT_ADVANCED_MIN_RATIO: float = 0.75   # >= 75%
    PLACEMENT_RETAKE_COOLDOWN_DAYS: int = 7
    PLACEMENT_QUESTIONS_COUNT: int = 20
    PLACEMENT_BASE_XP: int = 50

    # Module Quizzes & Gating Config (Requirements Update v2 - Section B)
    MODULE_QUIZ_QUESTIONS_COUNT: int = 15
    MODULE_QUIZ_PASS_THRESHOLD_RATIO: float = 0.65  # 65% of 15 = 9.75 -> 10 correct
    MODULE_QUIZ_PASS_MIN_CORRECT: int = 10
    MODULE_BANK_MIN_QUESTIONS: int = 40

    # XP System Rules (Requirements Update v2 - Section C)
    XP_BASE_FIXED: int = 10
    XP_PER_CORRECT_ANSWER: int = 2
    XP_FIRST_PASS_BONUS: int = 50
    XP_PERFECT_SCORE_BONUS: int = 25
    XP_RETAKE_BASE_RATIO: float = 0.20  # 20% of base XP on retakes after a pass

    # ATS Scoring Weights (Requirements Update v2 - Section E)
    ATS_WEIGHT_ROLE_FIT: float = 0.40
    ATS_WEIGHT_KEYWORD_COVERAGE: float = 0.25
    ATS_WEIGHT_SECTION_COMPLETENESS: float = 0.15
    ATS_WEIGHT_FORMATTING: float = 0.10
    ATS_WEIGHT_QUANTIFIED_IMPACT: float = 0.10

    @property
    def effective_database_url(self) -> str:
        """Resolves SQLite path consistently to backend/novapath.db."""
        if self.DATABASE_URL and self.DATABASE_URL.strip():
            db_url = self.DATABASE_URL.strip()
            if db_url.startswith("sqlite:///./"):
                rel_path = db_url.replace("sqlite:///./", "")
                abs_path = (_backend_dir / rel_path).resolve().as_posix()
                return f"sqlite:///{abs_path}"
            return db_url
        abs_default = (_backend_dir / "novapath.db").resolve().as_posix()
        return f"sqlite:///{abs_default}"

    # Network & Origins
    FRONTEND_ORIGIN: str = "http://localhost:5173"
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Legacy/Fallback keys
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    @property
    def effective_jwt_secret(self) -> str:
        """Prefers JWT_SECRET, falls back to SECRET_KEY if set, otherwise default."""
        if self.JWT_SECRET and self.JWT_SECRET != "change-me":
            return self.JWT_SECRET
        if self.SECRET_KEY:
            return self.SECRET_KEY
        return self.JWT_SECRET or "super-secret-jwt-key-for-hackathon-vizag-2026"

    @property
    def CORS_ORIGINS(self) -> List[str]:
        origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "*"
        ]
        if self.FRONTEND_ORIGIN and self.FRONTEND_ORIGIN not in origins:
            origins.insert(0, self.FRONTEND_ORIGIN)
        return origins

    @property
    def is_ai_available(self) -> bool:
        """Returns True only when OMNIROUTE_API_KEY is non-empty."""
        return bool(self.OMNIROUTE_API_KEY and self.OMNIROUTE_API_KEY.strip())

    @property
    def effective_chatbox_api_key(self) -> str:
        """
        Dedicated API key used ONLY for the AI Chatbox/Mentor.
        If CHATBOX_API_KEY is explicitly configured, it is used exclusively.
        Otherwise falls back to OMNIROUTE_API_KEY.
        """
        if self.CHATBOX_API_KEY and self.CHATBOX_API_KEY.strip():
            return self.CHATBOX_API_KEY.strip()
        return self.OMNIROUTE_API_KEY.strip()

    @property
    def is_chatbox_available(self) -> bool:
        """Returns True if either a dedicated CHATBOX_API_KEY or OMNIROUTE_API_KEY is set."""
        return bool(self.effective_chatbox_api_key)


settings = Settings()


def log_startup_config():
    """Logs backend configuration with secrets and keys strictly masked."""
    lines = [
        "=" * 65,
        "  NovaPath AI Backend -- Configuration Loaded",
        "=" * 65,
        f"  PROJECT_NAME:               {settings.PROJECT_NAME}",
        f"  VERSION:                    {settings.VERSION}",
        f"  PORT:                       {settings.PORT}",
        f"  FRONTEND_ORIGIN:            {settings.FRONTEND_ORIGIN}",
        f"  DATABASE_URL:               {'[SET]' if settings.DATABASE_URL else '[NOT SET]'}",
        f"  JWT_SECRET:                 {'[SET]' if settings.effective_jwt_secret != 'change-me' else '[DEFAULT/UNCONFIGURED]'}",
        f"  OMNIROUTE_BASE_URL:         {settings.OMNIROUTE_BASE_URL}",
        f"  OMNIROUTE_MODEL:            {settings.OMNIROUTE_MODEL}",
        f"  OMNIROUTE_FAST_MODEL:       {settings.OMNIROUTE_FAST_MODEL or '[NOT SET]'}",
        f"  OMNIROUTE_STRONG_MODEL:     {settings.OMNIROUTE_STRONG_MODEL or '[NOT SET]'}",
        f"  OMNIROUTE_TIMEOUT_SECONDS:  {settings.OMNIROUTE_TIMEOUT_SECONDS}s",
        f"  OMNIROUTE_API_KEY:          {'[SET]' if settings.is_ai_available else '[NOT SET]'}",
        "-" * 65
    ]
    if not settings.is_ai_available:
        lines.append("  [!] WARNING: OMNIROUTE_API_KEY is not set.")
        lines.append("      AI features marked unavailable (GET /api/ai/health -> ok:false).")
        lines.append("      To enable AI, add your key to backend/.env and restart.")
    else:
        lines.append("  [OK] OMNIROUTE_API_KEY is configured. AI features enabled.")
    lines.append("=" * 65)

    formatted = "\n".join(lines)
    logger.info(formatted)
    print(formatted, flush=True)
