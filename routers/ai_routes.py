from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from collections import defaultdict

from db_pt import DatabaseManager
from models_pt import Project

router = APIRouter()


@router.get("/ai/projects-summary")
def summary(db: Session = Depends(get_db)):
    projects = db.query(Project).all()

    return {
        "total": len(projects),
        "completed": len([p for p in projects if p.p_status == "Completed"]),
    }
