from pydantic import BaseModel
from typing import Optional, Dict

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class DiscoveryRequest(BaseModel):
    subreddit: str
    limit: Optional[int] = 10

class SaveIdeaRequest(BaseModel):
    idea_title: str
    idea_description: str
    pain_point_source: str
    market_potential: str
    concept_data: Optional[Dict] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TrendRequest(BaseModel):
    limit_sessions: Optional[int] = 50
    include_predictions: Optional[bool] = True
    include_alerts: Optional[bool] = True

class TrendDetectionRequest(BaseModel):
    hours_back: Optional[int] = 24
    enable_monitoring: Optional[bool] = False 