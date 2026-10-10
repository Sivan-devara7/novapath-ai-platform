from fastapi import APIRouter, Query
from typing import List, Optional
from ..models.schemas import ResourceItem
from ..services.rag_service import rag_service

router = APIRouter(prefix="/resources", tags=["resources"])

@router.get("/{skill_id}", response_model=List[ResourceItem])
async def get_resources_by_skill(
    skill_id: str,
    q: Optional[str] = None,
    type: Optional[str] = "all"
):
    return rag_service.search_resources(skill_id=skill_id, query=q or "", resource_type=type or "all")

@router.get("/", response_model=List[ResourceItem])
async def search_all_resources(
    q: Optional[str] = None,
    type: Optional[str] = "all"
):
    return rag_service.search_resources(skill_id="all", query=q or "", resource_type=type or "all")
