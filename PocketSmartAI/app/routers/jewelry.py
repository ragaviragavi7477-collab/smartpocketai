from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_optional_user
from app.models import User, RecommendationHistory
from typing import Optional
from app.schemas import JewelryPlannerInput, RecommendationResponse
from app.services.recommendation_service import get_jewelry_recommendations

router = APIRouter(prefix="/jewelry", tags=["Jewelry Planner"])

@router.post("/generate-jewelry", response_model=RecommendationResponse)
def generate_jewelry(data: JewelryPlannerInput, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_user)):
    recommendations = get_jewelry_recommendations(data)
    if current_user is not None:
        history = RecommendationHistory(
            user_id=current_user.id,
            category="Jewelry",
            budget=data.budget,
            prompt_data=str(data.model_dump()),
            recommendations=str(recommendations),
        )
        db.add(history)
        db.commit()
    return RecommendationResponse(category="Jewelry", recommendations=recommendations, total_budget=data.budget)
