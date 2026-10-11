import json
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from ..models.schemas import UserProfile
from ..models.db_models import User
from ..core.database import get_db
from ..services.document_service import document_service
from ..services.ats_service import ats_service

router = APIRouter(prefix="/profile", tags=["profile"])

DEMO_USER_ID = "usr-aarav-sharma"

@router.get("/me", response_model=UserProfile)
async def get_my_profile(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfile(**user.to_profile_dict())

@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    target_role: str = Form("AI Engineer"),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    extracted_text = document_service.extract_text_from_pdf(contents, file.filename)
    analysis = ats_service.analyze_resume_text(extracted_text, target_role)
    
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if user:
        current_skills = json.loads(user.verified_skills_json) if user.verified_skills_json else []
        for skill in analysis.extracted_skills:
            if skill not in current_skills:
                current_skills.append(skill)
        user.verified_skills_json = json.dumps(current_skills)
        db.commit()
        db.refresh(user)
        updated_skills = current_skills
    else:
        updated_skills = analysis.extracted_skills
        
    return {
        "filename": file.filename,
        "extracted_text_snippet": extracted_text[:400] + "...",
        "analysis": analysis,
        "verified_skills_updated": updated_skills
    }

@router.post("/upload-certificate")
async def upload_certificate(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    cert_info = document_service.parse_certificate(contents, file.filename)
    
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if user:
        current_skills = json.loads(user.verified_skills_json) if user.verified_skills_json else []
        for s in cert_info["skills_credited"]:
            if s not in current_skills:
                current_skills.append(s)
        user.verified_skills_json = json.dumps(current_skills)
        db.commit()

    return {
        "filename": file.filename,
        "certificate_metadata": cert_info,
        "message": f"Verified {len(cert_info['skills_credited'])} competencies added to student record."
    }
