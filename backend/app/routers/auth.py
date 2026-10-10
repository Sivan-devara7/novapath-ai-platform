from fastapi import APIRouter, HTTPException, status
from ..models.schemas import UserLogin, UserCreate, Token, UserProfile

router = APIRouter(prefix="/auth", tags=["auth"])

# Preloaded demo user for immediate hackathon zero-friction testing
DEMO_USER = UserProfile(
    id="usr-aarav-sharma",
    name="Aarav Sharma",
    email="aarav.sharma@vizag.edu",
    role="student",
    career_goal="AI Engineer",
    avatar="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
    streak=14,
    points=860,
    mastery_overall=72,
    radar_data=[
        {"subject": "Deep Learning", "A": 85, "fullMark": 100},
        {"subject": "System Design", "A": 65, "fullMark": 100},
        {"subject": "Algorithms", "A": 90, "fullMark": 100},
        {"subject": "MLOps", "A": 55, "fullMark": 100},
        {"subject": "Cloud & Infra", "A": 70, "fullMark": 100},
        {"subject": "Applied RAG", "A": 68, "fullMark": 100},
    ],
    verified_skills=["Python", "PyTorch", "Linear Algebra", "Git", "Docker"]
)

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    return Token(
        access_token="mock-jwt-token-aarav-sharma-2026",
        token_type="bearer",
        user=DEMO_USER
    )

@router.post("/demo-login", response_model=Token)
async def demo_login():
    """Instant 1-click login for judges and hackathon live presentations"""
    return Token(
        access_token="mock-jwt-token-aarav-sharma-2026",
        token_type="bearer",
        user=DEMO_USER
    )

@router.post("/signup", response_model=Token)
async def signup(user_data: UserCreate):
    new_user = UserProfile(
        id=f"usr-{abs(hash(user_data.email)) % 10000}",
        name=user_data.name,
        email=user_data.email,
        career_goal=user_data.career_goal,
        streak=1,
        points=100,
        mastery_overall=35,
        radar_data=[
            {"subject": "Deep Learning", "A": 40, "fullMark": 100},
            {"subject": "System Design", "A": 35, "fullMark": 100},
            {"subject": "Algorithms", "A": 50, "fullMark": 100},
            {"subject": "MLOps", "A": 20, "fullMark": 100},
            {"subject": "Cloud & Infra", "A": 30, "fullMark": 100},
            {"subject": "Applied RAG", "A": 25, "fullMark": 100},
        ],
        verified_skills=["Python"]
    )
    return Token(
        access_token=f"mock-jwt-token-{new_user.id}",
        token_type="bearer",
        user=new_user
    )
