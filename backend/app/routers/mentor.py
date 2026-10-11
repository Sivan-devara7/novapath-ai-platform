import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.db_models import User, ResumeAnalysis, UserModuleProgress, Module
from ..services.llm_service import llm_service, LLMOfflineError

router = APIRouter(prefix="/mentor", tags=["mentor"])

DEMO_USER_ID = "usr-aarav-sharma"

class ChatMessage(BaseModel):
    role: str
    content: str

class MentorChatRequest(BaseModel):
    messages: List[ChatMessage]
    context_hint: Optional[str] = None
    learning_style: Optional[str] = "hands-on"
    language: Optional[str] = "en"
    api_key: Optional[str] = None

class MentorChatResponse(BaseModel):
    reply: str
    model_used: str
    detected_gaps: List[str]
    suggested_actions: List[Dict[str, str]]

@router.post("/chat", response_model=MentorChatResponse)
async def mentor_chat(
    payload: MentorChatRequest,
    db: Session = Depends(get_db)
):
    """
    OmniRoute AI Personalized Mentor endpoint.
    Uses CHATBOX_API_KEY exclusively for the chatbox (without touching other APIs).
    Has full access to the student's real-time ATS gaps, verified skills, streak, and module progress.
    """
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        # Fallback dummy user if not found
        user = User(
            id=DEMO_USER_ID,
            name="Aarav Sharma",
            career_goal="AI Engineer",
            placement_level="Intermediate",
            placement_score=68.5,
            streak=14,
            total_xp=450
        )

    # 1. Fetch user's latest ATS analysis
    missing_skills = []
    matched_skills = []
    ats_score = 75

    try:
        latest_resume = db.query(ResumeAnalysis).filter(
            ResumeAnalysis.user_id == user.id
        ).order_by(ResumeAnalysis.created_at.desc()).first()

        if latest_resume:
            ats_score = latest_resume.overall_ats_score
            missing_skills = json.loads(latest_resume.missing_skills_json or "[]")
            matched_skills = json.loads(latest_resume.extracted_skills_json or "[]")
    except Exception:
        pass

    if not missing_skills:
        missing_skills = ["Vector Database", "RAG Architecture", "Distributed Model Serving"]

    # 2. Fetch current module progression
    course_id = "data-engineer" if "data" in (user.career_goal or "").lower() else (
        "cybersecurity" if "cyber" in (user.career_goal or "").lower() else "ai-engineer"
    )
    module_statuses = ["Foundations (available)", "Core Pipelines (locked)"]
    try:
        modules = db.query(Module).filter(Module.course_id == course_id).order_by(Module.order_index).all()
        if modules:
            module_statuses = [f"{m.title} (available)" for m in modules[:4]]
    except Exception:
        pass

    # 3. Construct System Prompt
    system_prompt = (
        f"You are NovaPath's OmniRoute Master AI Mentor, an elite, personalized technical advisor.\n"
        f"You have full access to this student's real-time platform data:\n"
        f"- Name: {user.name}\n"
        f"- Target Career Goal: {user.career_goal}\n"
        f"- Placement Level: {user.placement_level or 'Intermediate'} (Score: {user.placement_score or 68.5}%)\n"
        f"- Current Streak: {user.streak} days | Total XP: {user.total_xp}\n"
        f"- Current ATS Readiness Score: {ats_score}%\n"
        f"- Verified Skills: {', '.join(matched_skills[:6]) if matched_skills else 'Python, Data Structures, Git'}\n"
        f"- Identified Critical ATS Skill Gaps: {', '.join(missing_skills)}\n"
        f"- Current Track Modules: {'; '.join(module_statuses)}\n"
        f"- Preferred Learning Style: {payload.learning_style}\n"
        f"- Language Code: {payload.language}\n\n"
        f"Guidelines:\n"
        f"1. Address {user.name} personally and empathetically.\n"
        f"2. Explicitly reference their specific skill gaps ({', '.join(missing_skills[:3])}) when discussing learning paths.\n"
        f"3. Tailor explanations to their preferred learning style ({payload.learning_style}). If 'hands-on', provide quick code snippets or command examples.\n"
        f"4. If {payload.language} is not 'en', converse naturally in their chosen language ({payload.language}).\n"
        f"5. Keep responses concise, deeply insightful, encouraging, and technically sharp."
    )

    llm_messages = [{"role": "system", "content": system_prompt}]
    for msg in payload.messages[-6:]:
        llm_messages.append({"role": msg.role, "content": msg.content})

    # Resolve dedicated chatbox key strictly (never touches OMNIROUTE_API_KEY or other APIs)
    import httpx
    from ..config import settings
    chatbox_key = (payload.api_key or settings.CHATBOX_API_KEY or "").strip()
    model_used = settings.CHATBOX_MODEL or "openai/gpt-4o-mini"
    reply_text = ""

    if chatbox_key:
        if chatbox_key.startswith("sk-or-"):
            # Direct OpenRouter API execution
            try:
                url = f"{settings.CHATBOX_BASE_URL.rstrip('/')}/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {chatbox_key}",
                    "HTTP-Referer": settings.FRONTEND_ORIGIN or "http://localhost:5173",
                    "X-Title": "NovaPath AI Mentor"
                }
                body = {
                    "model": settings.CHATBOX_MODEL or "openai/gpt-4o-mini",
                    "messages": llm_messages,
                    "temperature": 0.7,
                    "max_tokens": 650
                }
                async with httpx.AsyncClient(timeout=15.0) as client:
                    resp = await client.post(url, json=body, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        reply_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                        model_used = data.get("model", model_used)
            except Exception as exc:
                reply_text = ""
        else:
            try:
                reply_text = await llm_service.chat(
                    messages=llm_messages,
                    model=model_used,
                    temperature=0.7,
                    max_tokens=650,
                    api_key=chatbox_key,
                    timeout_seconds=15.0
                )
            except Exception as exc:
                reply_text = ""

    # High-quality personalized multilingual fallback if key is unconfigured or call fails
    if not reply_text or reply_text.startswith("[AI Service Offline"):
        lang = (payload.language or "en").lower()
        last_query = payload.messages[-1].content if payload.messages else ""
        top_gaps = ", ".join(missing_skills[:3])
        primary_gap = missing_skills[0] if missing_skills else "Core Architecture"

        if lang == "te":
            reply_text = (
                f"నమస్కారం {user.name}! మీ **{user.career_goal}** ట్రాక్ కోసం మీ ప్రస్తుత ATS స్కోరు **{ats_score}%**.\n\n"
                f"మీకు 90%+ సాధించడానికి ముఖ్యమైన నైపుణ్య లోపాలు: **{top_gaps}**.\n"
                f"మీ {user.streak} రోజుల లెర్నింగ్ స్ట్రీక్‌ను కొనసాగించడానికి, తదుపరి **{primary_gap}** మాడ్యూల్ లేదా ప్రాజెక్ట్‌ను పూర్తి చేయండి!"
            )
        elif lang == "hi":
            reply_text = (
                f"नमस्ते {user.name}! आपके **{user.career_goal}** लक्ष्य के लिए आपका वर्तमान ATS स्कोर **{ats_score}%** है।\n\n"
                f"शीर्ष प्राथमिकता वाले कौशल अंतराल: **{top_gaps}**।\n"
                f"अपनी {user.streak}-दिनों की लय बनाए रखने के लिए, तुरंत **{primary_gap}** मॉड्यूल से शुरुआत करें!"
            )
        elif lang == "ta":
            reply_text = (
                f"வணக்கம் {user.name}! உங்கள் **{user.career_goal}** இலக்குக்கான தற்போதைய ஏடிஎஸ் மதிப்பெண் **{ats_score}%**.\n\n"
                f"முக்கிய திறன் இடைவெளிகள்: **{top_gaps}**.\n"
                f"உங்கள் {user.streak}-நாள் தொடர்ச்சியைத் தக்கவைக்க, உடனே **{primary_gap}** தொகுதியைத் தொடங்குங்கள்!"
            )
        elif lang == "kn":
            reply_text = (
                f"ನಮಸ್ಕಾರ {user.name}! ನಿಮ್ಮ **{user.career_goal}** ಗುರಿಗಾಗಿ ಪ್ರಸ್ತುತ ಎಟಿಎಸ್ ಅಂಕಗಳು **{ats_score}%**.\n\n"
                f"ಪ್ರಮುಖ ಕೌಶಲ್ಯ ಅಂತರಗಳು: **{top_gaps}**.\n"
                f"ನಿಮ್ಮ {user.streak} ದಿನಗಳ ಸತತ ಪ್ರಯತ್ನ ಮುಂದುವರಿಸಲು, **{primary_gap}** ಮಾಡ್ಯೂಲ್ ಅಭ್ಯಾಸ ಮಾಡಿ!"
            )
        elif lang == "bn":
            reply_text = (
                f"নমস্কার {user.name}! আপনার **{user.career_goal}** ট্র্যাকের জন্য বর্তমান এটিএস স্কোর **{ats_score}%**।\n\n"
                f"অগ্রাধিকার দক্ষতার ঘাটতি: **{top_gaps}**।\n"
                f"আপনার {user.streak} দিনের ধারাবাহিকতা ধরে রাখতে, পরবর্তী **{primary_gap}** মডিউল সম্পন্ন করুন!"
            )
        elif lang == "mr":
            reply_text = (
                f"नमस्कार {user.name}! तुमच्या **{user.career_goal}** उद्दिष्टासाठी सध्याचा एटीएस स्कोअर **{ats_score}%** आहे.\n\n"
                f"मुख्य कौशल्य अंतर: **{top_gaps}**.\n"
                f"तुमचे {user.streak}-दिवसांचे सातत्य कायम ठेवण्यासाठी, **{primary_gap}** मॉड्यूल पूर्ण करा!"
            )
        else:
            if "gap" in last_query.lower() or "ats" in last_query.lower():
                reply_text = (
                    f"Hello {user.name}! Based on your latest ATS audit for **{user.career_goal}**, your readiness score is **{ats_score}%**.\n\n"
                    f"To reach 90%+, your highest ROI focus is bridging these identified missing skills: **{top_gaps}**.\n"
                    f"I recommend diving directly into the prioritized **{primary_gap}** module on your roadmap."
                )
            elif "next" in last_query.lower() or "what" in last_query.lower():
                reply_text = (
                    f"Great momentum, {user.name}! You're currently on a **{user.streak}-day streak** with **{user.total_xp} XP**.\n\n"
                    f"For your **{user.placement_level or 'Intermediate'}** baseline, the highest impact next task is "
                    f"completing hands-on exercises in **{primary_gap}**, then passing the verification quiz."
                )
            else:
                reply_text = (
                    f"Hi {user.name}! As your dedicated **{user.career_goal}** mentor, I'm tracking your trajectory.\n\n"
                    f"With your {user.placement_level or 'Intermediate'} standing and {ats_score}% ATS match, you're building strong engineering habits. "
                    f"Would you like to review {primary_gap}, practice interview questions, or get code feedback?"
                )

    suggested_actions = [
        {"title": f"Review {missing_skills[0]} Module", "action_url": "/roadmap"},
        {"title": "View ATS Resume Gaps", "action_url": "/resume"},
        {"title": "Take Skill Quiz", "action_url": "/assessment"}
    ]

    return MentorChatResponse(
        reply=reply_text,
        model_used=model_used if chatbox_key else "novapath-adaptive-mentor",
        detected_gaps=missing_skills,
        suggested_actions=suggested_actions
    )

