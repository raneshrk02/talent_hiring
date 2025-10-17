from pymongo import MongoClient #type: ignore
from .config import settings

client = MongoClient(settings.DATABASE_URL)
db = client['talent_hiring']
candidates_collection = db['candidates']

def get_mongo_db():
    return db

def get_candidates_collection():
    return candidates_collection