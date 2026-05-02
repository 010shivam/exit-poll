import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    HASH_SECRET = os.getenv("HASH_SECRET")
    APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")