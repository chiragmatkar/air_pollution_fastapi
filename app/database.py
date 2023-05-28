import motor.motor_asyncio
import os

def get_database():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    return client.air
   

def get_collection():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db = client.air
    return db.get_collection(os.environ["MONGODB_COLLECTION"])
   
