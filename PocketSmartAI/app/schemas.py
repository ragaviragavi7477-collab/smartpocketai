from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool

class HomePlannerInput(BaseModel):
    budget: float = Field(..., gt=0)
    room_type: str
    room_quantity: int = Field(..., gt=0)
    lights_count: int = Field(default=0, ge=0)
    ceiling_fans: int = Field(default=0, ge=0)
    dining_tables: int = Field(default=0, ge=0)
    preferences: Optional[str] = None

class PartyPlannerInput(BaseModel):
    budget: float = Field(..., gt=0)
    guest_count: int = Field(..., gt=0)
    event_type: str
    venue: Optional[str] = None
    preferences: Optional[str] = None

class JewelryPlannerInput(BaseModel):
    budget: float = Field(..., gt=0)
    occasion: str
    style: str
    outfit_image_url: Optional[str] = None

class RecommendationResponse(BaseModel):
    category: str
    recommendations: List[dict]
    total_budget: float
    currency: str = "INR"

class HistoryResponse(BaseModel):
    id: int
    category: str
    budget: float
    recommendations: str
    created_at: datetime

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class UserInDB(BaseModel):
    id: int
    email: str
    username: str
    hashed_password: str
    is_active: bool
