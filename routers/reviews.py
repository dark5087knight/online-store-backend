from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Review

router = APIRouter(prefix="/api/reviews", tags=["reviews"])

@router.get("/all", response_model=list[Review])
def get_all_reviews(session: Session = Depends(get_session)):
    return session.exec(select(Review)).all()

@router.delete("/{id}")
def delete_review(id: str, session: Session = Depends(get_session)):
    review = session.get(Review, id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    session.delete(review)
    session.commit()
    return {"ok": True}
