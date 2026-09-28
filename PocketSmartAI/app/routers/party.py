from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_optional_user
from app.models import User, RecommendationHistory
from typing import Optional
from app.schemas import PartyPlannerInput, RecommendationResponse
from app.services.recommendation_service import get_party_recommendations

router = APIRouter(prefix="/party", tags=["Party Planner"])

@router.post("/generate-party", response_model=RecommendationResponse)
def generate_party(data: PartyPlannerInput, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_user)):
    recommendations = get_party_recommendations(data)
    if current_user is not None:
        history = RecommendationHistory(
            user_id=current_user.id,
            category="Party",
            budget=data.budget,
            prompt_data=str(data.model_dump()),
            recommendations=str(recommendations),
        )
        db.add(history)
        db.commit()
    return RecommendationResponse(category="Party", recommendations=recommendations, total_budget=data.budget)
