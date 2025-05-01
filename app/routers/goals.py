from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, auth, database

router = APIRouter(prefix="/goals", tags=["Goals"])

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- CRUD Operations -----------
@router.post("/", response_model=schemas.GoalOut)
def create_goal(goal: schemas.GoalCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_goal = models.Goal(**goal.model_dump(), user_id= current_user.id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.get("/", response_model=List[schemas.GoalOut])
def read_goals(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Goal).filter(models.Goal.user_id == current_user.id).all()

@router.get("/{goal_id}", response_model=schemas.GoalOut)
def read_out(goal_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    goal = db.query(models.Goal).filter(models.Goal.id == goal_id, models.Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    return goal

@router.put("/{goal_id}", response_model=schemas.GoalOut)
def update_goal(goal_id: int, updated_goal: schemas.GoalCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    goal = db.query(models.Goal).filter(models.Goal.id == goal_id, models.Goal.user_id == current_user.id).first()

    if not goal:
        raise HTTPException(status_code=404, details="Goal not found")
    
    for field, value in updated_goal.model_dump().items():
        setattr(goal, field, value)

    db.commit()
    db.refresh(goal)
    return goal

@router.delete("/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    goal = db.query(models.Goal).filter(models.Goal.id == goal_id, models.Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    db.delete(goal)
    db.commit()
    return {"detail": "Goal deleted successfully."}
