import json
import os
from sqlmodel import Session
from database import engine, init_db
from models import Category, Product, Review

def seed():
    # Make sure tables exist
    init_db()

    catalog_path = os.path.join(os.path.dirname(__file__), "..", "shopsphere-ai", "catalog.json")
    if not os.path.exists(catalog_path):
        print("catalog.json not found!")
        return

    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with Session(engine) as session:
        # Check if already seeded
        existing = session.query(Category).first()
        if existing:
            print("Database already seeded!")
            return

        print("Seeding Categories...")
        for cat_data in data.get("categories", []):
            cat = Category(**cat_data)
            session.add(cat)
        
        session.commit()

        print("Seeding Products and Reviews...")
        for prod_data in data.get("products", []):
            reviews_data = prod_data.pop("reviews", [])
            product = Product(**prod_data)
            session.add(product)
            session.commit() # commit product to get ID for reviews

            for rev_data in reviews_data:
                rev = Review(**rev_data, product_id=product.id)
                session.add(rev)
            
            session.commit()

        print("Seeding completed successfully!")

if __name__ == "__main__":
    seed()
