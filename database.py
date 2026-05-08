import os
import time
from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create engine, echo=True helps debug SQL queries during development
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    max_retries = 10
    retry_delay = 15

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempting to connect to the database (Attempt {attempt}/{max_retries})...")
            SQLModel.metadata.create_all(engine)
            print("Successfully connected to the database and initialized tables.")
            break
        except Exception as e:
            print(f"Database connection failed: {e}")
            if attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Could not connect to the database.")
                raise e

def get_session():
    with Session(engine) as session:
        yield session
