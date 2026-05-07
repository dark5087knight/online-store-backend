import sys
import time
import logging
from psycopg2 import OperationalError as Psycopg2OpError
from sqlalchemy.exc import OperationalError

from create_db import create_database
from seed_db import seed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def run():
    MAX_RETRIES = 10
    RETRY_DELAY = 10
    
    # -------------------------
    # STEP 1: Create DB
    # -------------------------
    db_created = False
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Attempting to create database (Attempt {attempt}/{MAX_RETRIES})...")
            create_database()
            db_created = True
            break
        except (Psycopg2OpError, Exception) as e:
            logger.error(f"Failed to create database: {e}")
            if attempt < MAX_RETRIES:
                logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error("Max retries reached. Exiting.")
                sys.exit(1)

    if not db_created:
        sys.exit(1)

    # -------------------------
    # STEP 2: Seed DB
    # -------------------------
    db_seeded = False
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Attempting to seed database (Attempt {attempt}/{MAX_RETRIES})...")
            seed()
            db_seeded = True
            logger.info("Database seeding process finished successfully!")
            break
        except (OperationalError, Exception) as e:
            logger.error(f"Failed to seed database: {e}")
            if attempt < MAX_RETRIES:
                logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error("Max retries reached. Exiting.")
                sys.exit(1)

    if not db_seeded:
        sys.exit(1)

if __name__ == "__main__":
    run()
