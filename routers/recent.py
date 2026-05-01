from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models import RecentActivity
from pydantic import BaseModel
import time

router = APIRouter(prefix="/api/recent", tags=["recent"])

class RecentAdd(BaseModel):
    user_id: str
    productId: str

@router.get("/", response_model=list[str])
def get_recent(user_id: str, session: Session = Depends(get_session)):
    items = session.exec(
        select(RecentActivity)
        .where(RecentActivity.user_id == user_id)
        .order_by(RecentActivity.timestamp.desc())
        .limit(12)
    ).all()
    return [item.productId for item in items]

@router.post("/")
def add_recent(data: RecentAdd, session: Session = Depends(get_session)):
    # Remove existing if any
    existing = session.exec(select(RecentActivity).where(
        RecentActivity.user_id == data.user_id, RecentActivity.productId == data.productId
    )).first()
    if existing:
        session.delete(existing)
        session.commit()
        
    new_item = RecentActivity(user_id=data.user_id, productId=data.productId, timestamp=time.time())
    session.add(new_item)
    session.commit()
    return {"status": "added"}
