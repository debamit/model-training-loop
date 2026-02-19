from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .goal import GoalType


class StepType(str, Enum):
    USER_INPUT = "user_input"
    TOOL_CALL = "tool_call"
    LLM_RESPONSE = "llm_response"
    VERIFICATION = "verification"


class JourneyStep(BaseModel):
    step_type: StepType
    description: str
    timestamp: datetime = datetime.utcnow()
    tool_name: Optional[str] = None
    input_data: Optional[dict] = None
    output_data: Optional[dict] = None


class Journey(BaseModel):
    id: str
    goal_id: str
    goal_type: GoalType
    steps: list[JourneyStep] = []
    started_at: datetime = datetime.utcnow()
    completed_at: Optional[datetime] = None
    status: str = "in_progress"
