from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from ..models.schemas import UserProfile
from ..services.document_service import document_service
from ..services.ats_service import ats_service
from .auth import DEMO_USER

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/me", response_model=UserProfile)
async def get_my_profile():
    return DEMO_USER

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...), target_role: str = Form("AI Engineer")):
    contents = await file.read()
    extracted_text = document_service.extract_text_from_pdf(contents, file.filename)
    analysis = ats_service.analyze_resume_text(extracted_text, target_role)
    
    # Merge newly discovered skills into profile
    for skill in analysis.extracted_skills:
        if skill not in DEMO_USER.verified_skills:
            DEMO_USER.verified_skills.append(skill)
            
    return {
        "filename": file.filename,
        "extracted_text_snippet": extracted_text[:400] + "...",
        "analysis": analysis,
        "verified_skills_updated": DEMO_USER.verified_skills
    }

@router.post("/upload-certificate")
async def upload_certificate(file: UploadFile = File(...)):
    contents = await file.read()
    cert_info = document_service.parse_certificate(contents, file.filename)
    
    for s in cert_info["skills_credited"]:
        if s not in DEMO_USER.verified_skills:
            DEMO_USER.verified_skills.append(s)

    return {
        "filename": file.filename,
        "certificate_metadata": cert_info,
        "message": f"Verified {len(cert_info['skills_credited'])} competencies added to student record."
    }
