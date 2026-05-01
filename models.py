from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, JSON

class Category(SQLModel, table=True):
    slug: str = Field(primary_key=True)
    name: str
    image: str
    tagline: str

class Product(SQLModel, table=True):
    id: str = Field(primary_key=True)
    slug: str
    title: str
    brand: str
    description: str
    price: float
    compareAtPrice: Optional[float] = None
    images: List[str] = Field(sa_column=Column(JSON))
    categorySlug: str = Field(foreign_key="category.slug")
    colors: List[str] = Field(sa_column=Column(JSON))
    sizes: List[str] = Field(sa_column=Column(JSON))
    rating: float
    reviewCount: int
    stock: int
    badges: List[str] = Field(sa_column=Column(JSON))
    tags: List[str] = Field(sa_column=Column(JSON))

class Review(SQLModel, table=True):
    id: str = Field(primary_key=True)
    product_id: str = Field(foreign_key="product.id")
    user: str
    rating: int
    title: str
    body: str
    date: str
    images: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

class UserAddress(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str # We'll just use a simple string for user identifier for now
    name: str
    line1: str
    line2: Optional[str] = None
    city: str
    region: str
    postal: str
    country: str
    phone: str
    isDefault: bool = False

class Order(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str
    date: str
    status: str # "processing", "shipped", "delivered", "cancelled"
    subtotal: float
    shipping: float
    tax: float
    total: float
    address_id: str = Field(foreign_key="useraddress.id")
    trackingSteps: List[dict] = Field(sa_column=Column(JSON))

class OrderItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    order_id: str = Field(foreign_key="order.id")
    productId: str
    title: str
    image: str
    price: float
    qty: int
    variant: dict = Field(sa_column=Column(JSON))

class CartItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    productId: str
    variant: dict = Field(sa_column=Column(JSON))
    qty: int
    savedForLater: bool = False

class WishlistItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    productId: str

class RecentActivity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    productId: str
    timestamp: float

class HeroBanner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    eyebrow: str
    title: str
    sub: str
    cta: str
    to_url: str
    params_slug: str
    image: str
    accent: str
