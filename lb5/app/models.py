from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Profile(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    phone: str  
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class ProfileCreate(BaseModel):
    username: str
    email: str
    full_name: str
    phone: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None