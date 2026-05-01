from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Product

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/", response_model=list[Product])
def get_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

@router.get("/{id}", response_model=Product)
def get_product(id: str, session: Session = Depends(get_session)):
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=Product)
def create_product(product: Product, session: Session = Depends(get_session)):
    existing = session.get(Product, product.id)
    if existing:
        raise HTTPException(status_code=400, detail="Product ID already exists")
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.put("/{id}", response_model=Product)
def update_product(id: str, product_data: Product, session: Session = Depends(get_session)):
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update fields
    update_data = product_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
        
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.delete("/{id}")
def delete_product(id: str, session: Session = Depends(get_session)):
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {"ok": True}
