import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # Connect to default postgres database
    conn = psycopg2.connect(
        dbname="postgres",
        user="dark",
        password="writeline",
        host="192.168.0.11",
        port="5432"
    )
    # Required to create databases
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    # Create the shopsphere database
    cursor.execute('CREATE DATABASE shopsphere')
    print("Database 'shopsphere' created successfully!")

    cursor.close()
    conn.close()
except psycopg2.errors.DuplicateDatabase:
    print("Database 'shopsphere' already exists!")
except Exception as e:
    print(f"Error creating database: {e}")
