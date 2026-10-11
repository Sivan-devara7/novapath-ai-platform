import json
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..models.schemas import UserLogin, UserCreate, Token, UserProfile
from ..models.db_models import User, XPEvent
from ..core.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

DEMO_USER_ID = "usr-aarav-sharma"

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
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return Token(
        access_token=f"jwt-token-{user.id}",
        token_type="bearer",
        user=UserProfile(**user.to_profile_dict())
    )

@router.post("/demo-login", response_model=Token)
async def demo_login(db: Session = Depends(get_db)):
    """Instant 1-click login for judges and hackathon live presentations"""
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="Demo user not found")
        
    return Token(
        access_token=f"jwt-token-{user.id}",
        token_type="bearer",
        user=UserProfile(**user.to_profile_dict())
    )

@router.post("/signup", response_model=Token)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already registered with this email")
        
    user_id = f"usr-{abs(hash(user_data.email)) % 100000}"
    new_user = User(
        id=user_id,
        name=user_data.name,
        email=user_data.email,
        hashed_password="mock-hashed-password",
        role="student",
        career_goal=user_data.career_goal,
        streak=1,
        total_xp=100,
        mastery_overall=35,
        radar_data_json=json.dumps([
            {"subject": "Deep Learning", "A": 40, "fullMark": 100},
            {"subject": "System Design", "A": 35, "fullMark": 100},
            {"subject": "Algorithms", "A": 50, "fullMark": 100},
            {"subject": "MLOps", "A": 20, "fullMark": 100},
            {"subject": "Cloud & Infra", "A": 30, "fullMark": 100},
            {"subject": "Applied RAG", "A": 25, "fullMark": 100},
        ]),
        verified_skills_json=json.dumps(["Python"])
    )
    db.add(new_user)
    db.add(XPEvent(
        user_id=new_user.id,
        source="signup_bonus",
        amount=100,
        metadata_json=json.dumps({"reason": "Welcome signup bonus"}),
        idempotency_key=f"signup-{new_user.id}"
    ))

    # Seed initial module progress: Module 1 available, subsequent locked
    from ..models.db_models import Module, UserModuleProgress
    modules = db.query(Module).filter(Module.course_id == "ai-engineer").order_by(Module.order_index).all()
    for mod in modules:
        db.add(UserModuleProgress(
            user_id=new_user.id,
            module_id=mod.id,
            status="available" if mod.order_index == 1 else "locked",
            best_score=0,
            attempts_count=0
        ))

    db.commit()
    db.refresh(new_user)

    return Token(
        access_token=f"jwt-token-{new_user.id}",
        token_type="bearer",
        user=UserProfile(**new_user.to_profile_dict())
    )
