from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Category

router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.get("/", response_model=list[Category])
def get_categories(session: Session = Depends(get_session)):
    categories = session.exec(select(Category)).all()
    return categories

@router.get("/{slug}", response_model=Category)
def get_category(slug: str, session: Session = Depends(get_session)):
    category = session.get(Category, slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=Category)
def create_category(category: Category, session: Session = Depends(get_session)):
    existing = session.get(Category, category.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Category slug already exists")
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

@router.put("/{slug}", response_model=Category)
def update_category(slug: str, category_data: Category, session: Session = Depends(get_session)):
    category = session.get(Category, slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    update_data = category_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
        
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

@router.delete("/{slug}")
def delete_category(slug: str, session: Session = Depends(get_session)):
    category = session.get(Category, slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}
