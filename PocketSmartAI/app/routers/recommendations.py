from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import RecommendationHistory, User
from app.schemas import HistoryResponse
from datetime import datetime

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/history", response_model=list[HistoryResponse])
def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    records = db.query(RecommendationHistory).filter(RecommendationHistory.user_id == current_user.id).order_by(RecommendationHistory.created_at.desc()).all()
    return [HistoryResponse(id=r.id, category=r.category, budget=r.budget, recommendations=r.recommendations, created_at=r.created_at) for r in records]

@router.get("/details/{category}", response_model=list[dict])
def get_recommendation_details(category: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    records = db.query(RecommendationHistory).filter(RecommendationHistory.user_id == current_user.id, RecommendationHistory.category == category).all()
    return [{"id": r.id, "category": r.category, "budget": r.budget, "recommendations": r.recommendations, "created_at": r.created_at} for r in records]
