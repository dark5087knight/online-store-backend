from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models import WishlistItem
from pydantic import BaseModel

router = APIRouter(prefix="/api/wishlist", tags=["wishlist"])

class WishlistToggle(BaseModel):
    user_id: str
    productId: str

@router.get("/", response_model=list[str])
def get_wishlist(user_id: str, session: Session = Depends(get_session)):
    items = session.exec(select(WishlistItem).where(WishlistItem.user_id == user_id)).all()
    return [item.productId for item in items]

@router.post("/")
def toggle_wishlist(data: WishlistToggle, session: Session = Depends(get_session)):
    existing = session.exec(select(WishlistItem).where(
        WishlistItem.user_id == data.user_id, WishlistItem.productId == data.productId
    )).first()
    
    if existing:
        session.delete(existing)
        session.commit()
        return {"status": "removed"}
    else:
        new_item = WishlistItem(user_id=data.user_id, productId=data.productId)
        session.add(new_item)
        session.commit()
        return {"status": "added"}

@router.delete("/clear/{user_id}")
def clear_wishlist(user_id: str, session: Session = Depends(get_session)):
    items = session.exec(select(WishlistItem).where(WishlistItem.user_id == user_id)).all()
    for item in items:
        session.delete(item)
    session.commit()
    return {"ok": True}
