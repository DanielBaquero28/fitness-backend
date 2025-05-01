from fastapi import APIRouter, Depends, HTTPException
from app import database, models, auth, schemas
from sqlalchemy.orm import Session
from typing import List

# API Base endpoint
router = APIRouter(prefix="/logs", tags=["Workout Logs"])

# Get DB dependency
def get_db():
    db = database.SessionLocal()
    print("Here 1")
    try:
        yield db
    finally:
        db.close()

# ------- CRUD Operations ---------
@router.post("/", response_model=schemas.WorkoutLogOut)
def create_log(log: schemas.WorkoutLogCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_log = models.WorkoutLog(**log.model_dump(), user_id=current_user.id)
    print(f"db_log: {db_log}")

    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return db_log

@router.get("/", response_model=List[schemas.WorkoutLogOut])
def read_logs(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.WorkoutLog).filter(models.WorkoutLog.user_id == current_user.id).all()

@router.get("/{log_id}", response_model=schemas.WorkoutLogOut)
def read_log(log_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    log = db.query(models.WorkoutLog).filter(models.WorkoutLog.id == log_id, models.WorkoutLog.user_id == current_user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Workout log not found")
    return log

@router.put("/{log_id}", response_model=schemas.WorkoutLogOut)
def update_log(log_id: int, updated_log: schemas.WorkoutLogCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    log = db.query(models.WorkoutLog).filter(models.WorkoutLog.id == log_id, models.WorkoutLog.user_id == current_user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Workout log not found")
    
    for field, value in updated_log.model_dump().items():
        setattr(log, field, value)

    db.commit()
    db.refresh(log)
    return log

@router.delete("/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)) -> dict:
    log = db.query(models.WorkoutLog).filter(models.WorkoutLog.id == log_id, models.WorkoutLog.user_id == current_user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Workout log not found")

    db.delete(log)
    db.commit()

    return {"detail": "Workout log deleted successfully"}