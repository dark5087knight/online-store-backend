from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import HeroBanner

router = APIRouter(prefix="/api/banners", tags=["banners"])

@router.get("/", response_model=list[HeroBanner])
def get_banners(session: Session = Depends(get_session)):
    return session.exec(select(HeroBanner)).all()

@router.post("/", response_model=HeroBanner)
def create_banner(banner: HeroBanner, session: Session = Depends(get_session)):
    session.add(banner)
    session.commit()
    session.refresh(banner)
    return banner

@router.put("/{id}", response_model=HeroBanner)
def update_banner(id: int, banner_data: HeroBanner, session: Session = Depends(get_session)):
    banner = session.get(HeroBanner, id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    
    for key, value in banner_data.dict(exclude_unset=True).items():
        if key != 'id':
            setattr(banner, key, value)
        
    session.add(banner)
    session.commit()
    session.refresh(banner)
    return banner

@router.delete("/{id}")
def delete_banner(id: int, session: Session = Depends(get_session)):
    banner = session.get(HeroBanner, id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    session.delete(banner)
    session.commit()
    return {"ok": True}
