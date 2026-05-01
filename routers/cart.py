from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import CartItem

router = APIRouter(prefix="/api/cart", tags=["cart"])

@router.get("/", response_model=list[CartItem])
def get_cart(user_id: str, session: Session = Depends(get_session)):
    items = session.exec(select(CartItem).where(CartItem.user_id == user_id)).all()
    return items

@router.post("/", response_model=CartItem)
def add_to_cart(item: CartItem, session: Session = Depends(get_session)):
    existing = session.exec(select(CartItem).where(
        CartItem.user_id == item.user_id,
        CartItem.productId == item.productId,
    )).all()
    
    for ex in existing:
        if ex.variant == item.variant and ex.savedForLater == item.savedForLater:
            ex.qty += item.qty
            session.add(ex)
            session.commit()
            session.refresh(ex)
            return ex
            
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.put("/{item_id}", response_model=CartItem)
def update_cart_item(item_id: int, item: CartItem, session: Session = Depends(get_session)):
    db_item = session.get(CartItem, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.qty = item.qty
    db_item.savedForLater = item.savedForLater
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def remove_from_cart(item_id: int, session: Session = Depends(get_session)):
    db_item = session.get(CartItem, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(db_item)
    session.commit()
    return {"ok": True}

@router.delete("/clear/{user_id}")
def clear_cart(user_id: str, session: Session = Depends(get_session)):
    items = session.exec(select(CartItem).where(CartItem.user_id == user_id)).all()
    for item in items:
        session.delete(item)
    session.commit()
    return {"ok": True}
