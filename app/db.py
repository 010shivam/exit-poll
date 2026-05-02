from flask_sqlalchemy import SQLAlchemy
import sqlite3
from config import Config

DB_NAME = Config.SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "")

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn



def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_hash TEXT UNIQUE,           
        vote TEXT,
        age_group TEXT,
        district TEXT,
        gender TEXT,
        voter_location TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()