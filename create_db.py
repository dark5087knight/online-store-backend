import os
from urllib.parse import urlparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import errors
from dotenv import load_dotenv

def create_database():
    load_dotenv()
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not found in .env file")

    parsed = urlparse(DATABASE_URL)
    DB_NAME = parsed.path.lstrip("/")
    DB_USER = parsed.username
    DB_PASSWORD = parsed.password
    DB_HOST = parsed.hostname
    DB_PORT = parsed.port or 5432

    try:
        # Connect to the default 'postgres' database to create the new one
        # Using connect_timeout to prevent hanging if the database server isn't reachable
        conn = psycopg2.connect(
            dbname= "postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            connect_timeout=10
        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if the database exists before creating it
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f"Database '{DB_NAME}' created successfully!")
        else:
            print(f"Database '{DB_NAME}' already exists!")

        cursor.close()
        conn.close()

    except errors.DuplicateDatabase:
        print(f"Database '{DB_NAME}' already exists!")
    except Exception as e:
        print(f"Error creating database: {e}")
        raise e
