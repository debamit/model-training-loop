from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Step(BaseModel):
    type: str
    tool: Optional[str] = None
    input: Optional[str] = None
    output: Optional[str] = None
    content: Optional[str] = None


class ConversationEntry(BaseModel):
    conversation_id: str
    steps: list[Step]
    tools_used: list[str] = []
    sources_checked: list[str] = []
    user_preference: Optional[str] = ""
    user_context: Optional[str] = ""


class GoalGroup(BaseModel):
    goal: str
    conversations: list[ConversationEntry]


class AnalysisOutput(BaseModel):
    date: str
    analyzed_at: str
    source_sessions: list[str]
    goals: list[GoalGroup]
