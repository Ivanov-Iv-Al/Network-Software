from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    user_email: str

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    user_email: str
    created_at: datetime
    updated_at: datetime

class StatusUpdate(BaseModel):
    status: str