from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class GoalType(str, Enum):
    PAYMENT = "payment"
    TRAVEL = "travel"
    RESEARCH = "research"
    GENERAL = "general"


class Goal(BaseModel):
    id: str
    user_intent: str
    goal_type: GoalType
    created_at: datetime = datetime.utcnow()
    constraints: list[str] = []
    metadata: dict = {}
