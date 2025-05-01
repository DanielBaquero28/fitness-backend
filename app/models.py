from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    goals = relationship("Goal", back_populates="owner")

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    target = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="goals")
    logs = relationship("WorkoutLog", back_populates="goal")

class WorkoutLog(Base):
    __tablename__ = "workout_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.now)
    type = Column(String)
    notes = Column(Text)
    duration = Column(Integer)

    goal_id = Column(Integer, ForeignKey("goals.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    goal = relationship("Goal", back_populates="logs")
    user = relationship("User")