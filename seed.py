import json
import os
from sqlmodel import Session
from database import engine, init_db
from models import Category, Product, Review


def load_catalog():
    # Lambda runs code from /var/task
    base_path = os.path.dirname(__file__)
    catalog_path = os.path.join(base_path, "catalog.json")

    if not os.path.exists(catalog_path):
        raise Exception("catalog.json not found")

    with open(catalog_path, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_database():
    # Ensure tables exist
    init_db()

    data = load_catalog()

    with Session(engine) as session:

        # Check if already seeded
        existing = session.query(Category).first()
        if existing:
            print("Database already seeded!")
            return

        # -------------------------
        # SEED CATEGORIES
        # -------------------------
        print("Seeding Categories...")
        categories = [
            Category(**cat_data)
            for cat_data in data.get("categories", [])
        ]
        session.add_all(categories)
        session.commit()

        # -------------------------
        # SEED PRODUCTS + REVIEWS
        # -------------------------
        print("Seeding Products and Reviews...")

        for prod_data in data.get("products", []):

            reviews_data = prod_data.pop("reviews", [])

            product = Product(**prod_data)
            session.add(product)
            session.commit()  # needed to get product.id

            reviews = [
                Review(**rev_data, product_id=product.id)
                for rev_data in reviews_data
            ]

            session.add_all(reviews)
            session.commit()

        print("Seeding completed successfully!")


# -------------------------
# CLI ENTRY POINT
# -------------------------
if __name__ == "__main__":
    try:
        seed_database()
        print("Database seeded successfully")
    except Exception as e:
        print("Seed failed:", str(e))
        import sys
        sys.exit(1)
