from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ---------- USER ------------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

# -------- GOAL ----------
class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    target: Optional[str] = None

class GoalCreate(GoalBase):
    pass

class GoalOut(GoalBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }

# --------- LOG -------
class WorkoutLogBase(BaseModel):
    type: str
    notes: Optional[str] = None
    duration: int

class WorkoutLogCreate(WorkoutLogBase):
    goal_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }

class WorkoutLogOut(WorkoutLogBase):
    id: int
    date: datetime
    goal_id: Optional[int]

    model_config = {
            "from_attributes": True
        }