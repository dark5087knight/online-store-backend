from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Order, OrderItem

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.get("/", response_model=list[Order])
def get_orders(user_id: str, session: Session = Depends(get_session)):
    orders = session.exec(select(Order).where(Order.user_id == user_id)).all()
    return orders

@router.post("/", response_model=Order)
def create_order(order: Order, session: Session = Depends(get_session)):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

@router.get("/all", response_model=list[Order])
def get_all_orders(session: Session = Depends(get_session)):
    return session.exec(select(Order)).all()

@router.put("/{id}", response_model=Order)
def update_order_status(id: str, status: str, trackingSteps: list[dict], session: Session = Depends(get_session)):
    order = session.get(Order, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    order.trackingSteps = trackingSteps
    session.add(order)
    session.commit()
    session.refresh(order)
    return order
